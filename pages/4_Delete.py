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

# Get thecard number to delete from user
def getCardNumbers(mycursor, user_name):
    query = 'SELECT Card_No from ' + user_name
    return ExecuteQuery(mycursor, query)

# Delete data from DB
def DeleteDB(mycursor, user_name, card_num):
    query = 'Delete from ' + user_name + ' where Card_No=%s'
    data=(card_num,)
    getFields_df = ExecuteQueryWithData(mycursor, query, data)
    return getFields_df

# View data after deleting
def RetrieveImageDetails(mycursor, user_name):
    query = 'SELECT * from ' + user_name
    st.dataframe(ExecuteQueryWithHeadings(mycursor, query))

# Streamlit page setup
st.set_page_config(
        page_title = "Delete data",
        page_icon =  ":heavy_multiplication_x:",
        initial_sidebar_state = "auto"
        )

# Retrieving the session state variables 
mycursor = ss['mycursor']
user_name = ss['user_name']
mydb = ss['mydb']

# Delete the existing data from DB
st.write("### :violet[Delete Records]")

card_df = getCardNumbers(mycursor,user_name)
if not card_df.empty:
        with st.form('delete_form'):
             card_num = st.selectbox('Select the card number to update',
                                     card_df,
                                     index=None)
             if(st.form_submit_button(':violet[Delete]')):
                DeleteDB(mycursor, user_name, card_num)
                RetrieveImageDetails(mycursor, user_name)
                mydb.commit()
else:
    st.write('No Records to Delete')

