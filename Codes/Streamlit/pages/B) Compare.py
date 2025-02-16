import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import time
import psycopg2

st.title("Compare Before & After Query Optimization 🔍")
st.write("")
st.write("")
st.write("")

def get_data(query):
    conn = st.session_state.db_connection
    df = pd.read_sql_query(query, conn)
    return df

# User Input Filters
category_filter = st.selectbox('Category', ['All'] + list(get_data("SELECT DISTINCT category FROM google_play_apps")['category']))
content_rating_filter = st.selectbox('Content Rating', ['All'] + list(get_data("SELECT DISTINCT content_rating FROM google_play_apps")['content_rating']))
editors_choice = st.selectbox('Editors Choice', ['All'] + list(get_data("SELECT DISTINCT editors_choice FROM google_play_apps")['editors_choice']))
rating_filter = st.slider('Rating', 0.0, 5.0, (2.5, 5.0))
price_filter = st.slider('price_usd (0 is considered as free)', 0.0, 400.0, (0.0, 10.0))

# Function to execute and measure query time
def measure_query_time(query, enable_index=True):
    conn = st.session_state.db_connection
    cursor = conn.cursor()
    if enable_index:
        cursor.execute("SET enable_indexscan = ON;")
    else:
        cursor.execute("SET enable_indexscan = OFF;")
    conn.commit()
    start_time = time.time()
    df = pd.read_sql_query(query, conn)
    end_time = time.time()
    execution_time = end_time - start_time
    return df, execution_time

# Build query based on filters
if st.button("Submit"):
    query = "SELECT * FROM google_play_apps WHERE 1=1"
    if category_filter != 'All':
        query += f" AND category = '{category_filter}'"
    if content_rating_filter != 'All':
        query += f" AND content_rating = '{content_rating_filter}'"
    if editors_choice != 'All':
        query += f" AND editors_choice = '{editors_choice}'"
    query += f" AND rating BETWEEN {rating_filter[0]} AND {rating_filter[1]}"
    query += f" AND price_usd BETWEEN {price_filter[0]} AND {price_filter[1]}"

        # Measure query time without index scan
    filtered_data_without_index, time_without_index = measure_query_time(query, enable_index=False)

    # Measure query time with index scan
    filtered_data_with_index, time_with_index = measure_query_time(query, enable_index=True)

    st.write(f"Time for indexed scan: {round(time_with_index, 2)} seconds")
    st.write(f"Time for sequential scan (without indexing): {round(time_without_index, 2)} seconds")
    
    # Display filtered data
    st.write(filtered_data_with_index)

# Close the connection when the app stops
@st.cache_resource
def close_connection():
    conn = st.session_state.db_connection
    conn.close()

# st.on_event("shutdown", close_connection)
