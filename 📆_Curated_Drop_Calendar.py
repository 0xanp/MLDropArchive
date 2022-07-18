import streamlit as st
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import pathlib
import os
import data_processor as dp

# ---- LOAD DATA ----
@st.experimental_memo
def load_data():
    return dp.load_data()

# ---- PAGE CONFIG ----
st.set_page_config(
     page_title="ML Curated Drop Calendar",
     page_icon=":waxing_crescent_moon:",
     layout="wide",
     initial_sidebar_state="expanded",
 )

# ---- HEADER ----
st.markdown("<p style= 'text-align: center;'> &#127770 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127770</p>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: white;'>Midnightlabs Curated Drop Calendar</h1>", unsafe_allow_html=True)
st.markdown("<p style= 'text-align: center;'> &#127770 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127770</p>", unsafe_allow_html=True)

# ---- DISPLAYING THE TABLE DESCRIPTION ----
with st.expander("Description"):
    st.markdown("""
        <p>
        Projects highlighted in
        <strong> <span style="color: #32CD32">green </span> </strong>
        were found to have strong fundumentals and potential to be mid-to-long term holds. <br> Projects in
        <strong> <span style="color: #FFFF00">yellow</span> </strong>
        are on our watchlist and will continue to be monitored as they develop. <br> Projects highlighted in
        <strong> <span style="color: #FF4500">orange</span> </strong>
        show signs of potential but lack important information needed to make a final call. 
        <br> Projects in <strong> <span style="color:#add8e6">light blue</span> </strong> were reviewed but were not added to the curated calendar. 
        </p>
    """,unsafe_allow_html=True)

# ---- LOAD ALL DATA ----
df = load_data()

# ---- SIDE BAR ----
cycle = st.sidebar.multiselect(
    "Cycle:",
    options=df["Cycle"].unique()[::-1],
    default=df["Cycle"].unique()[-1]
)

all_cycle_checkbox = st.sidebar.checkbox("All Cycle")
all = df["Cycle"].unique()

status = st.sidebar.multiselect(
    "Status:",
    options=["Green", "Yellow", "Orange"],
    default=["Green", "Yellow", "Orange"]
)

minted = st.sidebar.checkbox("Already Minted")

if minted:
    mint_date_query = ""
else:
    mint_date_query = "& `Mint Date` != 'Already Minted'"

clear_cache = st.sidebar.button('↻ Refresh')

if clear_cache:
    st.experimental_memo.clear()

if all_cycle_checkbox:
    cycle_query = "Cycle in @all"
else:
    cycle_query = "Cycle == @cycle"

df = df.query(cycle_query + "& Status == @status" + mint_date_query).sort_values(by=['status_num','Cycle'])[["Project","Twitter","Description","Mint Date","Cycle"]]


# ---- HIDING DEFAUT WATERMARK ----
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# ---- DISPLAYING THE TABLE ----
with st.container():
    st.write(df.to_html(escape=False), unsafe_allow_html=True)