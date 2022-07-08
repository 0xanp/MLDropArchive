import pandas as pd
from openpyxl import load_workbook
from urllib.request import urlopen
import requests

# ---- HYPERLINK ----
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{text}</a>'

# ---- TABLE STYLING ----
def coloring(s):
    color = 'green' if  s == 'green' else 'yellow' if s == 'yellow' else 'orange'
    return f'color: {color}'

# ---- READ EXCEL ----
def load_data():
    sheet_id = "1HLWkNCVi3mggBYVZNdHooP8KwTw47F7ATrmfKmvK6GY"
    gid = "1619771889"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    df = pd.read_excel(url)
    df = df[['Project','Mint Date','How Early','Twitter','JY Score','JY Comments','Guillermo Score','Guillermo Comments']]
    df = df[df['JY Score'].notnull() & df['Guillermo Score'].notnull()]
    df['Twitter'] = df['Twitter'].apply(make_clickable)
    #df['Comments'] = df['Comments'].str.replace("\n\n","").str.replace("\n \n","")
    df['Mint Date'] = df['Mint Date'].astype(str)
    return df

#df = load_data()
#print(df)