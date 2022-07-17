import pandas as pd
from datetime import datetime
import re
import numpy as np
# ---- HYPERLINK ----
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    #text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{link}</a>'

def custom_sort(df):
    df_mapping = pd.DataFrame({
    'status': ['Green', 'Yellow', 'Orange', 'Blue'],
    })
    sort_mapping = df_mapping.reset_index().set_index('status')
    df['status_num'] = df['Status'].map(sort_mapping['index'])
    return df

def format_desc(text):
    regex = r'\b(?:https?|telnet|gopher|file|wais|ftp):[\w/#~:.?+=&%@!\-.:?\\-]+?(?=[.:?\-]*(?:[^\w/#~:.?+=&%@!\-.:?\-]|$))'
    links = re.findall(regex, text)
    for link in links:
        text = text.replace(link, make_clickable(link))
    return text

def fill_nan(text):
    text  = "" if (text == "nan") else text
    return text

# ---- READ EXCEL ----
def load_data():
    sheet_id = "1HLWkNCVi3mggBYVZNdHooP8KwTw47F7ATrmfKmvK6GY"
    gid = "1619771889"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    df = pd.read_excel(url)
    df = df[['Project','Mint Date','Twitter','Status','Description','Date Last Reviewed','Picture Test']]
    df['Twitter'] = df['Twitter'].apply(make_clickable)
    df['Date Last Reviewed'] = df['Date Last Reviewed'].dt.strftime('%m/%d/%Y')
    df = df[df['Date Last Reviewed'].notna()]
    df = df[df['Status'].notna()]
    df = df[df['Project'].notna()]
    df = df[df['Status'] != 'Already Minted']
    df.loc[df["Status"] == "Green",'Project'] = "<a style='color:green;'>" + df.loc[df["Status"] == "Green",'Project'] + "</a>"
    df.loc[df["Status"] == "Orange",'Project'] = "<a style='color:orange;'>" + df.loc[df["Status"] == "Orange",'Project'] + "</a>"
    df.loc[df["Status"] == "Yellow",'Project'] = "<a style='color:yellow;'>" + df.loc[df["Status"] == "Yellow",'Project'] + "</a>"
    df.loc[df["Status"] == "Blue",'Project'] = "<a style='color:#add8e6;'>" + df.loc[df["Status"] == "Blue",'Project'] + "</a>"
    df = custom_sort(df)
    df.rename(columns = {'Date Last Reviewed':'Cycle'}, inplace = True)
    df["Mint Date"] = df['Mint Date'].apply(lambda x: pd.to_datetime(x).strftime('%m/%d/%Y') if type(x) is datetime else x)
    df["Description"] = df["Description"].astype(str).apply(fill_nan)
    df["Description"] = df["Description"].astype(str).apply(lambda x: x.replace("\n\n","<br> <br>"))
    df["Description"] = df["Description"].astype(str).apply(lambda x: x.replace("\n \n","<br> <br>"))
    df["Description"] = df["Description"].astype(str).apply(format_desc)
    pd.set_option('display.colheader_justify', 'left')
    return df.fillna(" ")

#df = load_data()
#print(df[df['Project']=="<a style='color:yellow;'>wagmiunited</a>"]['Picture Test'].astype(str))
#print(df[df['Project']=="<a style='color:#add8e6;'>Wakey-wakey</a>"]['Description'])