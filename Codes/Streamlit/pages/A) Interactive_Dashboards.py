import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Function to get data
def get_data(query):
    # Use the connection to execute the query
    conn = st.session_state.db_connection
    df = pd.read_sql_query(query, conn)
    return df

st.title("Interactive Dashboards 📊")
st.write("")
st.write("")
st.write("")

filtering = st.checkbox("Search Dashboards")
if filtering == True:
    st.write("## Filters")
    # Filter options
    category_filter = st.selectbox('Category', ['All'] + list(get_data("SELECT DISTINCT category FROM google_play_apps")['category']))
    content_rating_filter = st.selectbox('Content Rating', ['All'] + list(get_data("SELECT DISTINCT content_rating FROM google_play_apps")['content_rating']))
    editors_choice = st.selectbox('Editors Choice', ['All'] + list(get_data("SELECT DISTINCT editors_choice FROM google_play_apps")['editors_choice']))
    rating_filter = st.slider('Rating', 0.0, 5.0, (2.5, 5.0))
    price_filter = st.slider('price_usd (0 is considered as free)', 0.0, 400.0, (0.0, 10.0))

    see_filtered = st.button("Submit")
    if see_filtered:
        # Build query based on filters
        query = "SELECT * FROM google_play_apps WHERE 1=1"
        if category_filter != 'All':
            query += f" AND category = '{category_filter}'"

        if content_rating_filter != 'All':
            query += f" AND content_rating = '{content_rating_filter}'"

        if editors_choice != 'All':
            query += f" AND editors_choice = '{editors_choice}'"

        query += f" AND rating BETWEEN {rating_filter[0]} AND {rating_filter[1]}"
        query += f" AND price_usd BETWEEN {price_filter[0]} AND {price_filter[1]}"


        # Retrieve filtered data
        filtered_data = get_data(query)

        # Display data
        st.write("### Filtered Google Play Store Apps Data", filtered_data)

        # Data Visualization: Distribution of Ratings
        st.write("### Distribution of Ratings")
        fig, ax = plt.subplots()
        plt.title('Distribution of Ratings')
        sns.histplot(filtered_data['rating'], bins=20, kde=True, ax=ax)
        st.pyplot(fig)

        # Data Visualization: Average Ratings by Category
        st.write("### Average Ratings by Category")
        if 'category' in filtered_data.columns:
            avg_ratings = filtered_data.groupby('category')['rating'].mean().reset_index()
            fig, ax = plt.subplots(figsize=(15, 15))
            sns.barplot(x='rating', y='category', data=avg_ratings, color='red', ax=ax)
            st.pyplot(fig)

        # Make sure to close the connection when the app stops
        @st.cache_resource
        def close_connection():
            conn = st.session_state.db_connection
            conn.close()

        # st.on_event("shutdown", close_connection)

st.write('---------------------------------------------------------------------------------------------------------')


Rating_per_category = st.checkbox("Rating Average Per Category")
if Rating_per_category == True:
    st.write("## Filters")
    # Filter options
    category_filter_rating_per_avg = st.selectbox('Category', ['All'] + list(get_data("SELECT DISTINCT category FROM google_play_apps")['category']))
    
    use_order = st.selectbox("Do want to SORT the data?", ["Yes", "No"])
    if use_order == 'Yes':
        sort_type = st.selectbox("Which one?", ["Ascending", "Descending"])

    see_filtered_avg_category = st.button("Submit")

    if see_filtered_avg_category:
        query = "SELECT category, ROUND(CAST(AVG(rating) AS numeric), 2) AS rating_average FROM google_play_apps Where 1=1 "
        if category_filter_rating_per_avg != 'All':
            query += f" AND category = '{category_filter_rating_per_avg}' "

        query += f" GROUP BY category"

        if use_order == 'Yes':
            if sort_type == 'Ascending': sort_type = 'Asc'
            if sort_type == 'Descending': sort_type = 'Desc'

            query += f" order by rating_average {sort_type} "

        # Retrieve filtered data
        filtered_data = get_data(query)

        # Display data
        st.write("### Filtered Averaging Rate Per Category", filtered_data)

st.write('---------------------------------------------------------------------------------------------------------')

last_update = st.checkbox("Annual Update and Release Dates Analysis")
if last_update:
    # Filter options
    category = st.selectbox('Select Category', get_data("SELECT DISTINCT category FROM google_play_apps")['category'])

    # Query to get filtered data based on selected category
    query = f"SELECT * FROM google_play_apps WHERE category = '{category}'"
    data = get_data(query)

    # Convert date columns to datetime, handle 'Not Available' and other non-date values
    data['last_updated'] = pd.to_datetime(data['last_updated'], format='%b %d, %Y', errors='coerce')
    data['released'] = pd.to_datetime(data['released'], format='%b %d, %Y', errors='coerce')

    # Extract year from the date columns
    data['Update_Year'] = data['last_updated'].dt.year
    data['Release_Year'] = data['released'].dt.year

    # Group by year and count occurrences
    update_counts = data.groupby('Update_Year').size()
    release_counts = data.groupby('Release_Year').size()

    # Plot the time series
    fig, ax = plt.subplots(2, 1, figsize=(12, 15))

    # Update dates chart
    ax[0].plot(update_counts.index, update_counts.values, marker='o')
    ax[0].set_title('Annual Last Update Dates')
    ax[0].set_xlabel('Year')
    ax[0].set_xticks(np.arange(2010, 2024, 2))
    ax[0].set_ylabel('Number of Apps')
    ax[0].grid(True)

    # Release dates chart
    ax[1].plot(release_counts.index, release_counts.values, marker='o', color='orange')
    ax[1].set_title('Annual Released Dates')
    ax[1].set_xlabel('Year')
    ax[1].set_xticks(np.arange(2010, 2024, 2))
    ax[1].set_ylabel('Number of Apps')
    ax[1].grid(True)

    # Display the plots in Streamlit
    st.pyplot(fig)