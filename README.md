# NASA-Near-Earth-Object-NEO-Tracking-Insights-using-Public-API
This is a project that is made to take the information about asteroid approaches from a given URL using python and SQL and thus make a Streamlit UI to display the information derived.
The Python script automates the process of collecting data about Near Earth Objects (NEOs) from NASA's NEO API and storing it in a MySQL database
1. Importing Libraries
requests: This library is used to make HTTP requests to the NASA API. The script uses it to fetch the NEO data in JSON format.
2. Configuration
API_KEY:  This variable stores your NASA API key.  You'll need to replace the placeholder value with your actual API key obtained from the NASA API portal.
url: This variable holds the base URL for the NASA NEO Feed API.  The script will modify this URL to include date ranges and the API key.
target: This variable defines the number of asteroid records the script aims to collect. The script will continue fetching data until this target is reached.
Here a target of 10000 has been made.
4. Data Retrieval Loop
The core of the script is a while loop that continues as long as the number of collected asteroid records (len(asteroids_data)) is less than the specified target.
Fetching Data:
Inside the loop, the script uses the requests.get(url) function to send a GET request to the NASA API.  The API responds with NEO data in JSON format.
response.json():  The script converts the JSON response from the API into a Python dictionary, making it easier to work with the data.
Extracting Asteroid Details:
The script navigates the dictionary structure of the API response.  The  data['near_earth_objects']  key contains a dictionary where each key is a date, and the value is a list of asteroids that have close approaches on that date.
The code iterates through each date and each asteroid in the list.
Storing Data:
Each asteroid's data is stored as a dictionary, and this dictionary is appended to the asteroids_data list.
Loop Termination:
The loop includes checks to stop fetching data once the target number of asteroid records is collected.  It breaks out of the inner and outer loops.
Pagination:
 The NASA API provides a "next" link in the response, which points to the next page of results. The script updates the url variable with this link, allowing it to fetch data in pages.

5.Connecting with the database using pymysql.connect().

6. Database Interaction:
Creating the Table:
The script executes a SQL CREATE TABLE statement to create the asteroids table in your MySQL database.  
Inserting Data:
The script prepares an SQL INSERT statement with placeholders (%s) for the values.
It iterates through the asteroids_data list, which contains the dictionaries of asteroid information.
For each asteroid, it extracts the values and appends them as a tuple to the values list.
7.Taking up SQL Queries:
SQL queries has been made for various problems and is retrieved from the connected database.
8.Constructing a streamlit UI:
1. Importing Libraries:
streamlit as st : For creating the user interface.
pandas as pd : For working with data in a tabular format.
pymysql:  For connecting to the MySQL database.
datetime.date: For working with dates.
2.  App Title and State Management:
st.markdown():  Displays a formatted title for the application.
st.session_state: Streamlit's session state is used to manage the active tab in the application, ensuring the UI remains consistent across interactions.
3.  Sidebar Navigation:
st.sidebar:  Creates a sidebar for navigation.
The script defines a set_tab() function to update the active tab in the session state.
The sidebar displays two buttons, "Filter Range" and "Queries", which allow the user to switch between the two main sections of the application.
4.  Filter Range Tab:
st.subheader():  Displays a heading for the filter section.
The script defines a SQL query (data) with placeholders for filtering asteroid data based on user-selected criteria.
st.columns():  Divides the layout into columns for a more organized display of filter widgets.
The script uses various Streamlit widgets (st.slider(), st.date_input(), st.selectbox()) to create interactive filters.
When the "Apply Filters" button is clicked:
The script executes the SQL query with the selected filter values.
The results are fetched using cursor.fetchall().
The results are converted into a Pandas DataFrame.
The DataFrame is displayed using st.dataframe().
5. Queries Tab:
st.session_state.active_tab == "Queries": Displays heading for the Queries section.
st.selectbox():  Creates a dropdown menu for selecting pre-defined queries.
The script defines several elif blocks, one for each query:
Each query is a SQL statement designed to retrieve specific information about asteroids from the database.
The script executes the selected query.
The results are fetched, converted into a Pandas DataFrame, and displayed using st.dataframe().
And thus we get an interactive UI named 'NASA ASTEROID TRACKER'.


