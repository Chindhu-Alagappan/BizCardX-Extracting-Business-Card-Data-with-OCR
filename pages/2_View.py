# Import necessary packages
import streamlit as st
from streamlit import session_state as ss
import pandas as pd

# Executing MySQL queries
def ExecuteQuery(mycursor, query):
    mycursor.execute(query)
    res = mycursor.fetchall()
    field_headings = [i[0] for i in mycursor.description]
    return pd.DataFrame(res, columns = field_headings)

# Retrieving all data stored in DB
def RetrieveImageDetails(mycursor, user_name):
    query = 'SELECT * from '+user_name
    st.dataframe(ExecuteQuery(mycursor, query))

# Retrieving the session state variables
mycursor = ss['mycursor']
mydb = ss['mydb']
user_name = ss['user_name']

# Streamlit page setup
st.set_page_config(
        page_title = "View data",
        page_icon =  ":eyes:",
        initial_sidebar_state = "auto"
        )
# Viewing data in table format
st.write("### :violet[Image Processing data]")
RetrieveImageDetails(mycursor, user_name)
mydb.commit()



