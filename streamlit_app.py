from urllib.error import URLError

import pandas as pd
import requests
import snowflake.connector
import streamlit


def requests_fruityvice(fruit: str):
    URL: str = "https://fruityvice.com/api/fruit/"
    try:
        response: requests.Response = requests.get(f"{URL}{fruit}")
        return pd.json_normalize(response.json())
    except Exception as e:
        return {"error": e}


def get_fruit_load():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()


def insert_row_snoflake(new_fruit) -> str:
    with my_cnx.cursor() as my_cur:
        my_cur.execute(
            f"insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('{new_fruit}')")
        return f"Thanks for adding {new_fruit}"


streamlit.title("My parents new healthy diner")

streamlit.header("Breakfest menu")
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach and Rocket smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# creating dataframe and putting on the app
my_fruit_list: pd.DataFrame = pd.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(
    my_fruit_list.index), ["Avocado", "Strawberries"])

# Filtered df to show
df_to_show = my_fruit_list.loc[fruits_selected]

# Display df
streamlit.dataframe(df_to_show)

# New header
streamlit.header("Fruityvice Fruit Advice!")

# User input
try:
    fruit_choice = streamlit.text_input(
        'What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        fruityvice_normalized = requests_fruityvice(fruit=fruit_choice)
        streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error(e)

streamlit.header("The fruit load list contains:")
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

second_fruit_choice = streamlit.text_input('What fruit do you  like to add?')
if streamlit.button("Add a Fruit to the List"):
    if second_fruit_choice:
        with snowflake.connector.connect(**streamlit.secrets["snowflake"]) as my_cnx:
            back_insert = insert_row_snoflake(new_fruit=second_fruit_choice)
            streamlit.text(back_insert)
    else:
        streamlit.error("Please to input a valid name")
