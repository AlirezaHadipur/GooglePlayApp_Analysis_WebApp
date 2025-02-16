import streamlit as st
import pandas as pd
import psycopg2

st.title("CRUD Operations 🔄")
st.write("")
st.write("")
st.write("")
# ---------------------------------------------- CRUD ------------------------------------------------
# Create a new record
def Create(table, columns, values):
    conn = st.session_state.db_connection
    cursor = conn.cursor()
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
    cursor.execute(query, values)
    conn.commit()
    cursor.close()

# Read records
def Read(table):
    conn = st.session_state.db_connection
    query = f"SELECT * FROM {table}"
    df = pd.read_sql_query(query, conn)
    return df

# Update a record
def Update(table, set_columns, set_values, condition_column, condition_value):
    conn = st.session_state.db_connection
    cursor = conn.cursor()
    set_clause = ', '.join([f"{col} = %s" for col in set_columns])
    query = f"UPDATE {table} SET {set_clause} WHERE {condition_column} = %s"
    cursor.execute(query, set_values + [condition_value])
    conn.commit()
    cursor.close()

# Delete a record
def Delete(table, condition_column, condition_value):
    conn = st.session_state.db_connection
    cursor = conn.cursor()
    query = f"DELETE FROM {table} WHERE {condition_column} = %s"
    cursor.execute(query, (condition_value,))
    conn.commit()
    cursor.close()

# ---------------------------------------------- CRUD ------------------------------------------------

create_checked = st.checkbox("Create Record")
if create_checked:
    # User inputs for table and columns
    st.header("Specify Table and Features")
    table_name = st.text_input("Table Name")
    columns = st.text_area("Columns (comma-separated)").split(", ")
    values = st.text_area("Values (comma-separated)").split(", ")


    # Input fields for CRUD operations
    if st.button("Create"):
        Create(table_name, columns, values)
        st.success("Record created successfully!")

st.write('---------------------------------------------------------------------------------------------------------')

read_checked = st.checkbox("Read Table")
if read_checked:
    st.header("Read Records")
    table_name = st.text_input("Table Name for Reading")
    if st.button("Read"):
        records_df = Read(table_name)
        st.write(records_df)

st.write('---------------------------------------------------------------------------------------------------------')

update_checked = st.checkbox("Update Record")
if update_checked:
    st.header("Update a Record")
    table_name = st.text_input("Table Name for Updating")
    set_columns = st.text_area("Columns to Update (comma-separated)").split(", ")
    set_values = st.text_area("New Values (comma-separated)").split(", ")
    condition_column = st.text_input("Condition Column")
    condition_value = st.text_input("Condition Value")
    if st.button("Update"):
        Update(table_name, set_columns, set_values, condition_column, condition_value)
        st.success("Record updated successfully!")

st.write('---------------------------------------------------------------------------------------------------------')

delete_checked = st.checkbox("Delete Record")
if delete_checked:
    st.header("Delete a Record")
    table_name = st.text_input("Table Name for Deleting")
    del_condition_column = st.text_input("Condition Column for Deletion")
    del_condition_value = st.text_input("Condition Value for Deletion")
    if st.button("Delete"):
        Delete(table_name, del_condition_column, del_condition_value)
        st.success("Record deleted successfully!")
