import streamlit as st
import pandas as pd
import numpy as np
from openpyxl import load_workbook
import pathlib
import os
import data_processor as dp

# ---- LOAD DATA ----
@st.cache
def load_data():
    return dp.load_data()
# ---- PAGE CONFIG ----
st.set_page_config(page_title='ML Drop Calendar Archive',page_icon=":waxing_crescent_moon:", layout="wide")

# ---- HEADER ----
st.write(":waxing_crescent_moon: :first_quarter_moon: :waxing_gibbous_moon: :waxing_gibbous_moon: :full_moon: :waning_gibbous_moon: :last_quarter_moon: :waning_crescent_moon:")
st.title('Midnightlabs Drop Calendar Archive')
st.write(":waxing_crescent_moon: :first_quarter_moon: :waxing_gibbous_moon: :waxing_gibbous_moon: :full_moon: :waning_gibbous_moon: :last_quarter_moon: :waning_crescent_moon:")
st.markdown("""
    <p>
    <strong> Description: </strong> Projects highlighted in
    <span style="color: #32CD32">green</span>
    were found to have strong fundumentals and potential to be mid-to-long term holds. Projects in
    <span style="color: #FFFF00">yellow</span> 
    are on our watchlist and will continue to be monitored as they develop. Projects highlighted in
    <span style="color: #FF4500">orange</span> 
    show signs of potential but lack important information needed to make a final call.
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

status = st.sidebar.multiselect(
    "Status:",
    options=["Green", "Yellow", "Orange","Not Good Enough","Other","Non Ethereum"],
    default=["Green", "Yellow", "Orange"]
)

minted = st.sidebar.checkbox("Already Minted")

if minted:
    query = ""
else:
    query = "& `Mint Date` != 'Already Minted'"

df = df.query("Cycle == @cycle & Status == @status" + query).sort_values(by=['status_num'])[["Project","Twitter","Description","Mint Date","Cycle"]]


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
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)