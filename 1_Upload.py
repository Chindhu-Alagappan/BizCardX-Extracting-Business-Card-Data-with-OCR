# Import necessary packages
import streamlit as st
from PIL import Image
import easyocr
import pandas as pd
import numpy as np
import re
from streamlit import session_state as ss 
import base64

# Formatting the website field
def FormatWebSite(website):
    site = []
    for i in website:
        if ' ' in i or '.' in i:
            i.replace('.',' ')
            i = i.split()
            for x in i:
                x = x.lower()
                site.append(x)
        else:
            i = i.lower()
            site.append(i)
    return ".".join(site)

# Formatting the phone number field
def FormatPhoneNumber(numbers):
    for i in range(0,len(numbers)):
        if numbers[i][0] != '+':
            numbers[i] = '+'+numbers[i]
    numbers = ",".join(numbers)
    return numbers

number_regex = re.compile(r'^[0-9]+$')

# Formatting the address field
def FormatAddress(address):
    add = []
    for i in address:
        if ',' in i:
            i = i.replace(',',' ')
        if ';' in i:
            i = i.replace(';',' ')
        i = i.split()
        for x in i:
            x = x.title()
            add.append(x)
    for i in add:
        if number_regex.match(i) and len(i)<6:
            door_num = i # Door Number
        elif i == 'Abc' or i == 'Global':
            street_name = i # Street name
        elif i == 'St':
            street = i
        elif number_regex.match(i) and len(i)>=6:
            pincode = i
        elif i == 'Tamilnadu':
            state = i
        else:
            area = i
    address = door_num \
                + ", " \
                + street_name \
                + " " \
                + street \
                + ", " \
                + area \
                + ", " \
                + state \
                + ", " \
                + "Pincode - "\
                + pincode \
                + "."
    
    return address

# Formatting all the fields from the extracted image
def FormatImageDetailsExtracted(result, file_name):      
        phone_regex = re.compile(r'^[+\d\-]+\d$')
        web_regex_start= re.compile(r'^www',re.IGNORECASE)
        web_regex_end = re.compile(r'.+\.com$',re.IGNORECASE)
        company_name_regex = re.compile(r'^[a-zA-Z ]+$')

        # Creating a dictionary of fields
        fields={'Card_No':None,
                'Name':None,
                'Role':None, 
                'Company':[],
                'Email':None,
                'Phone':[],
                'Website':[],
                'Address':[]}

        # Extracting only the text data from the easy OCR output
        text_detected = []
        for detection in result:
                text_detected.append(detection[1])

        # Categorizing the data based on the fields
        fields['Card_No'] = file_name
        for i in range(0,len(text_detected)):
                if i == 0:
                     fields['Name'] = text_detected[i]
                elif i == 1:
                     fields['Role'] = text_detected[i]
                elif '@' in text_detected[i]:
                     fields['Email'] = text_detected[i]
                elif phone_regex.match(text_detected[i]) and len(text_detected[i]) > 6:
                     fields['Phone'].append(text_detected[i])
                elif web_regex_start.match(text_detected[i]):
                     fields['Website'].append(text_detected[i])
                elif web_regex_end.match(text_detected[i]):
                     fields['Website'].append(text_detected[i])
                elif company_name_regex.match(text_detected[i]):
                     fields['Company'].append(text_detected[i])
                else:
                     fields['Address'].append(text_detected[i])

        # Formatting each and every field 
        fields['Name'] = fields['Name'].title()
        fields['Role'] = fields['Role'].title()
        fields['Company'] = [i.title() for i in fields['Company']]
        fields['Company'] = " ".join(fields['Company'])
        fields['Email'] = fields['Email'].lower()
        fields['Address'] = FormatAddress(fields['Address'])
        fields['Phone'] = FormatPhoneNumber(fields['Phone'])
        fields['Website'] = FormatWebSite(fields['Website'])

        # Creating a empty dataframe and appending the results
        result_df = pd.DataFrame( columns=['Card_No',
                                           'Name',
                                           'Role',
                                           'Company',
                                           'Phone',
                                           'Email',
                                           'Website',
                                           'Address'])
        result_df.loc[len(result_df)] = fields

        return result_df, fields

# Creating table if not present in the DB
def CreateTable(mycursor, user_name):
     query = 'CREATE TABLE ' \
                + user_name \
                + ' (Card_No INT PRIMARY KEY, \
                        Name VARCHAR(255), \
                        Role VARCHAR(255), \
                        Company VARCHAR(255), \
                        Email VARCHAR(255), \
                        Phone VARCHAR(255), \
                        Website VARCHAR(255), \
                        Address TEXT, \
                        Image LONGBLOB)'
     
     mycursor.execute(query)

# Verifying the data - if the image is already present or not
def CheckIfDataAlreadyPresent(mycursor, user_name, find_card_num):
     query = 'select count(*) from '+ user_name +' where Card_No=%s'
     data = (find_card_num,)
     mycursor.execute(query,data)
     isPresent = 0
     for i in mycursor:
          isPresent = i[0]

     return isPresent

# Verifying the DB tables - if the table is already present or not
def CheckIfTableAlreadyPresent(mycursor, user_name):
    query = "SELECT COUNT(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_NAME = %s"
    data = (user_name,)
    mycursor.execute(query,data)
    tablepresent = 0
    for i in mycursor:
        tablepresent = i[0]

    # If no table found then create one
    if tablepresent == 0:
        CreateTable(mycursor, user_name)

# Inserting the extracted data to the DB
def InsertToDB(mycursor, result_dict, user_name, image):
    CheckIfTableAlreadyPresent(mycursor, user_name)
    
    isPresent = CheckIfDataAlreadyPresent(mycursor, 
                                          user_name, 
                                          result_dict['Card_No'])
    print(isPresent)

    mssg = ''
    if isPresent == 0:
        query = 'INSERT INTO ' \
                + user_name \
                +' (Card_No, Name, Role, Company, Email, Phone, Website, Address, Image) \
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        data = (result_dict['Card_No'], 
                result_dict['Name'], 
                result_dict['Role'], 
                result_dict['Company'], 
                result_dict['Email'], 
                result_dict['Phone'], 
                result_dict['Website'], 
                result_dict['Address'], 
                image)
        mycursor.execute(query,data)
        mssg = 'Data Inserted'

    elif isPresent > 0:
        mssg = 'Data Already Exists'
    return mssg

# Streamlit page setup
st.set_page_config(
        page_title = "Upload image",
        page_icon =  ":arrow_up:",
        initial_sidebar_state = "auto"
        )

# Session state variables initialization
if 'button_clicked' not in ss:
     ss.button_clicked = False 

# Retrieving the session state variables
mycursor = ss['mycursor']
mydb = ss['mydb']

# Extraction form
st.write("### :violet[Data Extraction from Image]")
try :
    with st.form('extract_form'):
        uploaded_file = st.file_uploader("Choose images to extract data...", 
                                         type=['png', 'jpg', 'jpeg'])
        extract_submitted = st.form_submit_button(':violet[Extract]')

    if extract_submitted or ss.button_clicked:
            ss.button_clicked = True
            image = Image.open(uploaded_file) 
            st.write(':violet[Original Image]')
            st.image(image) 
            status1 = st.empty()
            status1.write(':violet[Processing...]')
            reader = easyocr.Reader(['en'], gpu=False)
            result = reader.readtext(np.array(image))
            file_name = uploaded_file.name.split('.')[0]
            if(result is not None):
                    status1.write(':green[Image Processed Successfully.]')
                    with st.expander(":violet[View JSON Format]"):
                            st.json(result)

                    with st.expander(":violet[View Table Format]"):
                            result_df, result_dict = \
                                FormatImageDetailsExtracted(result,file_name)
                            st.write(result_df)

                    # Save to DB form
                    with st.form('save_form'):
                        st.write(':violet[Click to save the extracted data\
                                             to the database]')
                        save_submitted = st.form_submit_button(':violet[Save]')  
                        if save_submitted:
                            status2 = st.empty()
                            status2.write(':violet[Inserting to DB...]')
                            image_file = uploaded_file.read()
                            image_file = base64.b64encode(image_file)
                            mssg = InsertToDB(mycursor, 
                                              result_dict, 
                                              st.session_state['user_name'],
                                              image_file)
                            mydb.commit()
                            status2.write(':green[' + mssg + ']')

except Exception as e:
     st.write(':violet[Select the image before hitting "Extract" button]')
     print('Error Message'+str(e))