# from typing import Any

import pandas as pd
import requests
import streamlit


def requests_fruityvice(fruit: str):
    URL: str = "https://fruityvice.com/api/fruit/"
    try:
        response: requests.Response = requests.get(f"{URL}{fruit}")
        return response.json()
    except Exception as e:
        return {"error": e}


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

# Panting watermelon info
# streamlit.text(requests_fruityvice(fruit="watermelon"))
