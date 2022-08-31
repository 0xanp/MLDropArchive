import pandas as pd
from datetime import datetime
import re
import numpy as np
from dotenv import load_dotenv
import os

# ---- CREATING HYPERLINK ----
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">{link}</a>'

# ---- CUSTOM SORT RULE ----
def custom_sort(df):
    df_mapping = pd.DataFrame({
    'status': ['Green', 'Yellow', 'Orange'],
    })
    sort_mapping = df_mapping.reset_index().set_index('status')
    df['status_num'] = df['Status'].map(sort_mapping['index'])
    return df

# ---- HANDLING FORMAT OF IMAGES ----
def format_images(link):
    if link != 'nan':
        return f'<img src={link} width="80">'
    else:
        return ""

# ---- HANLDING FORMAT OF DESCRIPTION COLUMN ----
def format_description(text):
    regex = r'\b(?:https?|telnet|gopher|file|wais|ftp):[\w/#~:.?+=&%@!\-.:?\\-]+?(?=[.:?\-]*(?:[^\w/#~:.?+=&%@!\-.:?\-]|$))'
    links = re.findall(regex, text)
    for link in links:
        text = text.replace(link, make_clickable(link))
    return text

# ---- HANDLING NAN STRING ----
def fill_nan(text):
    text  = "" if (text == "nan") else text
    return text

# ---- READ EXCEL ----
def load_data():
    load_dotenv()
    # Reading from google sheets
    sheet_id = os.environ.get("SHEET_ID")
    gid = os.environ.get("GID")
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    df = pd.read_excel(url)
    # Querying necessary columns
    df = df[['Project','Mint Date','Twitter','Status','Description','Date Last Reviewed','Picture Test']]
    # Formatting links for twitter column
    df['Twitter'] = df['Twitter'].apply(make_clickable)
    # formatting datetime
    df['Date Last Reviewed'] = df['Date Last Reviewed'].dt.strftime('%m/%d/%Y')
    # Filtering null values from columns
    df = df[df['Date Last Reviewed'].notna()]
    df = df[df['Status'].notna()]
    df = df[df['Project'].notna()]
    df = df[df['Status'] != 'Already Minted']
    # Formatting Status Column
    df.loc[df["Status"] == "Green",'Project'] = "<a style='color:green;'>" + df.loc[df["Status"] == "Green",'Project'] + "</a>"
    df.loc[df["Status"] == "Orange",'Project'] = "<a style='color:orange;'>" + df.loc[df["Status"] == "Orange",'Project'] + "</a>"
    df.loc[df["Status"] == "Yellow",'Project'] = "<a style='color:yellow;'>" + df.loc[df["Status"] == "Yellow",'Project'] + "</a>"
    # Creating a custom sort rule based on colors/status
    df = custom_sort(df)
    # Renaming columns to be more explicit
    df.rename(columns = {'Date Last Reviewed':'Cycle'}, inplace = True)
    df.rename(columns = {'Picture Test':'Picture'}, inplace = True)
    # Formatting images' links
    df["Picture"] = df["Picture"].astype(str).apply(format_images)
    df["Mint Date"] = df['Mint Date'].apply(lambda x: pd.to_datetime(x).strftime('%m/%d/%Y') if type(x) is datetime else x)
    # Formatting Description Column
    df["Description"] = df["Description"].astype(str).apply(fill_nan)
    df["Description"] = df["Description"].astype(str).apply(lambda x: x.replace("\n\n","<br> <br>"))
    df["Description"] = df["Description"].astype(str).apply(lambda x: x.replace("\n \n","<br> <br>"))
    df["Description"] = df["Description"].astype(str).apply(lambda x: x.replace("\n","<br>"))
    df["Description"] = df["Description"].astype(str).apply(format_description)
    # Setting alignment for dataframe
    pd.set_option('display.colheader_justify', 'left')
    # Filling null values
    df = df.fillna(" ")
    # Creating a custom index system as represeting pictures
    df = df.set_index("Picture", drop=True)
    # Removing the name of the index column
    df.index.name = None
    return df
