from unicodedata import name
import streamlit as st
import pandas as pd
import numpy as np
import data_processor as dp
import datetime

# ---- LOAD DATA ----
@st.experimental_memo
def load_data():
    return dp.load_data()

# ---- HANDLING ALL PAGE CONFIGS ----
def page_config():
    # ---- PAGE CONFIG ----
    st.set_page_config(
        page_title="Curated Drop Calendar",
        page_icon=":waxing_crescent_moon:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ---- HEADER ----
    st.markdown("<p style= 'text-align: center;'> &#127770 &#127770 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127770 &#127770</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white;'>Midnight Labs Curated Drop Calendar</h1>", unsafe_allow_html=True)
    st.markdown("<p style= 'text-align: center;'> &#127770 &#127770 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127761 &#127762 &#127763 &#127764 &#127765 &#127766 &#127767 &#127768 &#127761 &#127770 &#127770</p>", unsafe_allow_html=True)

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
            </p>
        """,unsafe_allow_html=True)
    
    # ---- HIDING DEFAUT WATERMARK  AND ADDING SOCIALS----
    css_example ="""
             <style>
            #MainMenu {visibility: hidden; }
            footer {visibility: hidden; }
            a:link,
            a:visited {
            background-color: transparent;
            text-decoration: underline;
            }
            a:hover,
            a:active {
            color: red;
            background-color: transparent;
            text-decoration: underline;
            }
            </style>                                                                                                                                      
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <div style= 'text-align: center;'>
                <a target="_blank" href="https://www.joinmidnightlabs.com/"><i class="fa-solid fa-window-maximize fa-xl"></i></a>                                                                                                                                                                                                                                                                                            
                <a target="_blank" href="https://twitter.com/midnightlabshq"><i class="fa-brands fa-twitter fa-xl"></i></a>
                <a target="_blank" href="https://discord.com/invite/vAxZapwM98"><i class="fa-brands fa-discord fa-xl"></i></a>
            </div>
            <br><br><br>
    """
    st.sidebar.markdown(css_example, unsafe_allow_html=True)


# ---- HANDLING CONVERSION FROM DATAFRAME TO CSV ----
def df_to_raw_csv(df):
    for column in df.columns:
        df[column] = df[column].str.replace(r'<[^<>]*>', '', regex=True)
    return df.to_csv().encode('utf-8')

# ---- HANDLING CONVERSION FROM DATAFRAME TO CSV ----

def main():
    # ---- LOAD ALL PAGE CONFIG ----
    page_config()

    # ---- LOAD ALL DATA ----
    df = load_data()
    
    # ---- SIDE BAR ----
    cycle = st.sidebar.multiselect(
        "❍ Cycle:",
        options=[pd.to_datetime(x, "%m/%d/%Y").strftime("%m/%d/%Y") for x in sorted(df["Cycle"].unique(),reverse=True)],
        default=[pd.to_datetime(x, "%m/%d/%Y").strftime("%m/%d/%Y") for x in sorted(df["Cycle"].unique(),reverse=True)][0]
    )

    all_cycle_checkbox = st.sidebar.checkbox("All Cycle")
    all = df["Cycle"].unique()

    status = st.sidebar.multiselect(
        "❍ Status:",
        options=["Green", "Yellow", "Orange"],
        default=["Green", "Yellow", "Orange"]
    )

    minted = st.sidebar.checkbox("Already Minted")

    # ---- FILTERING LOGIC ----
    if minted:
        mint_date_query = ""
    else:
        mint_date_query = "& `Mint Date` != 'Already Minted'"

    if all_cycle_checkbox:
        cycle_query = "Cycle in @all"
    else:
        cycle_query = "Cycle == @cycle"
    
    
    # ---- QUERYING FROM DATAFRAME ----
    df = df.query(cycle_query + "& Status == @status" + mint_date_query).sort_values(by=['status_num','Cycle'])[["Project","Twitter","Description","Mint Date","Cycle"]]
    df["Cycle"] = df["Cycle"].apply(lambda x: x.strftime("%m/%d/%Y"))
    df_html = df.to_html(escape=False)
    df_csv = df_to_raw_csv(df)
    
    # ---- DOWNLOAD BUTTON ----
    st.sidebar.download_button(
        label="Export Current Table as HTML",
        data=df_html,
        file_name='current_data.html',
        mime='text/html',
    )
    st.sidebar.download_button(
        label="Export Current Table as CSV",
        data=df_csv,
        file_name='current_data.csv',
        mime='text/csv',
    )
    # ---- REFRESH BUTTON ----
    clear_cache = st.sidebar.button('↻ Refresh')

    if clear_cache:
        st.experimental_memo.clear()

    # ---- DISPLAYING THE TABLE ----
    with st.container():
        st.write(df_html, unsafe_allow_html=True) 

if __name__ == "__main__":
    main()