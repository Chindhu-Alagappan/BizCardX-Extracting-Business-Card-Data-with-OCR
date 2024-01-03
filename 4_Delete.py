# Import necessary packages
import streamlit as st
from streamlit import session_state as ss
import Bizcard as bc 

# Delete data from DB
def DeleteDB(mycursor, user_name, card_num):
    query = 'Delete from ' + user_name + ' where Card_No=%s'
    data=(card_num,)
    getFields_df = bc.ExecuteQueryWithData(mycursor, query, data)
    return getFields_df

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

card_df = bc.getCardNumbers(mycursor,user_name)
if not card_df.empty:
        with st.form('delete_form'):
             card_num = st.selectbox('Select the card number to update',
                                     card_df,
                                     index=None)
             if(st.form_submit_button(':violet[Delete]')):
                DeleteDB(mycursor, user_name, card_num)
                bc.RetrieveImageDetails(mycursor, user_name)
                mydb.commit()
else:
    st.write('No Records to Delete')

