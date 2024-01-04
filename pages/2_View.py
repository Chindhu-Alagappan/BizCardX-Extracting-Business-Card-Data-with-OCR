# Import necessary packages
import streamlit as st
from streamlit import session_state as ss
from Bizcard import RetrieveImageDetails

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



