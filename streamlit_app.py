import streamlit

import pandas

import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('Build your Smoothie')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# create a function
def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice) # get fruit details from fruityvue api response
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) # normalize the data
     return fruityvice_normalized
    
#new section to display fruityvue api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?') # fruit selection input
    if not fruit_choice:
        streamlit.error("Please select a fruit.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function) # present data in a table format
    
except URLError as e:
       streamlit.error()
        
    
streamlit.header("The fruit load list contains:")
#testing snowflake connection
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("select * from fruit_load_list")
          return my_cur.fetchall()

# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
          my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
          my_data_rows = get_fruit_load_list()
          streamlit.dataframe(my_data_rows)
          
# don't run anything past this line
# streamlit.stop()

# allow user to add a fruid to the list
add_my_fruit = streamlit.text_input("What fruit would you like information about?")
if streamlit.button("Add a Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)


