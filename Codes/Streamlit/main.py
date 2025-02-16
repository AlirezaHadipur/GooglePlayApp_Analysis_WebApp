import streamlit as st
import pandas as pd
import numpy as np
import psycopg2


st.title("Welcome To My Webapp:computer:")
st.write("## This webapp is build by __Alireza Hadipoor__ :smile:")
st.write("")
st.write("")
st.write("")
st.write("")

st.write("##### You can find useful information about Google Play Apps on this webapp :iphone:")
st.write("Here are some quick navigations:")
st.write(" 1) You can see __Interactive Dashboards__ and filter data. 📊")
st.write(" 2) You can Compare Before and After __Query Optimization__ in Compare section. 🔄")
st.write(" 3) You can Create, Read, Update, and Delete data using __CRUD__. 🛠️")



# Function to create a database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="ADB_FinalProject",
        user="postgres",
        password="hadipoor1379"
    )

# Store the connection in session_state
if 'db_connection' not in st.session_state:
    st.session_state.db_connection = get_db_connection()
