# Import necessary packages
import streamlit as st
import mysql.connector
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

# Retrieving all data stored in DB
def RetrieveImageDetails(mycursor, user_name):
    query = 'SELECT * from '+user_name
    st.dataframe(ExecuteQueryWithHeadings(mycursor, query))

# -------------Retrieving the CardNumbers to Update-----------------------------
def getCardNumbers(mycursor, user_name):
    query = 'SELECT Card_No from '+user_name
    return ExecuteQuery(mycursor, query)

# ------------ Main Method --------------------------------------------
def main():
    # Initialize session user name as user1
    user_name = 'User1'
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = user_name

    # Connecting with MySQL 
    mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'Chinka@SQL123',
        db = 'bizcardx'
    )

    # Initialize session state variables
    st.session_state['mydb'] = mydb
    mycursor = mydb.cursor()
    st.session_state['mycursor'] = mycursor

    # Streamlit page setup
    st.set_page_config(
        page_title = "BizCardX",
        page_icon =  ":credit_card",
        initial_sidebar_state = "auto"
        )
    
    # Contents of the Home page
    welcome_statement = "Welcome to BizCardX !"
    st.title(':violet[' + welcome_statement + ']')

    st.write('~ An interactive tool for Business Card Data Extraction. ')
    st.markdown(
        """
        We are living in a Digital Era, where data exists in various forms. \
        Images and videos play a vital role in conveying information. \
        So, it becomes utmost important to process them and extract meaningfull insights. 

        Here, we present you an interactive tool for processing business cards using the image processing techniques, storing and manipulating them using SQL - MySQL database.
        
        Developed by Chindhu, as an open-source project. Do leave your comments or suggestions of the portal, so that it can be revised and improved.

        Email - chindhual@gmail.com
        """
    )

if __name__ == "__main__":
    main()