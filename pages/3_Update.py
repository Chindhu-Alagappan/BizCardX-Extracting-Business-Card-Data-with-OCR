# Import necessary packages
import streamlit as st
from streamlit import session_state as ss
import pandas as pd

# --------------Executing MySQL queries--------------------------------

def ExecuteQuery(mycursor, query):
    mycursor.execute(query)
    res = mycursor.fetchall()
    return pd.DataFrame(res)

def ExecuteQueryWithData(mycursor, query, data):
    mycursor.execute(query, data)
    res = mycursor.fetchall()
    return pd.DataFrame(res)

def ExecuteQueryWithHeadings(mycursor, query):
    mycursor.execute(query)
    res = mycursor.fetchall()
    field_headings = [i[0] for i in mycursor.description]
    return pd.DataFrame(res, columns = field_headings)

# -------------Retrieving fields to Update-----------------------------
def getCardNumbers(mycursor, user_name):
    query = 'SELECT Card_No from '+user_name
    return ExecuteQuery(mycursor, query)

def getFields(mycursor, user_name, mydb):
    query = 'SELECT * FROM information_schema.columns WHERE table_schema = %s and table_name = %s'
    data = (mydb.database, user_name)
    getFields_df = ExecuteQueryWithData(mycursor, query, data)
    field_df = getFields_df.iloc[1:-1, 3:4]
    return field_df

# Update the extracted data
def UpdateDB(mycursor, user_name, field, new_value, card_num):
    query = 'Update '+ user_name +' set '+ field +' = %s where Card_No=%s'
    data = (new_value, card_num)
    getFields_df = ExecuteQueryWithData(mycursor,query,data)
    return getFields_df

# View the updated table
def RetrieveImageDetails(mycursor, user_name):
    query = 'SELECT * from '+user_name
    st.dataframe(ExecuteQueryWithHeadings(mycursor, query))

# Streamlit page setup
st.set_page_config(
        page_title = "Update data",
        page_icon =  ":arrows_counterclockwise:",
        initial_sidebar_state = "auto"
        )

# Retrieving the session state variables 
mycursor = ss['mycursor']
user_name = ss['user_name']
mydb = ss['mydb']

# Updating the stored data
st.write("### :violet[Update existing data]")

card_df = getCardNumbers(mycursor, user_name)
if not card_df.empty:
    with st.form('update_form'):
        card_num = st.selectbox('Select the card number to update', 
                                card_df,
                                index=None)
        field = st.selectbox('Select the field to update', 
                             getFields(mycursor, user_name, mydb),
                             index=None)
        new_value = st.text_input('Enter the new value of the field')
        if(st.form_submit_button(':violet[Update]')):
            UpdateDB(mycursor, user_name, field, new_value, card_num)
            RetrieveImageDetails(mycursor, user_name)
            mydb.commit()
else:
    st.write('No Records to Update')
