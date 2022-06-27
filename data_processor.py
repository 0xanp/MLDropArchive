import pandas as pd
from openpyxl import load_workbook
from urllib.request import urlopen
import requests

sheet_id = "1dqcnijkto5tx6aeOamqz38X14ZehmrdpiqhHX1CGNJc"
gid = "1651523875"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
df = pd.read_excel(url, usecols='A:E',skiprows=[1])
wb = load_workbook(url, data_only = True)
sh = wb[wb.sheetnames[0]]
print(sh['A3'].fill.start_color.index)



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
    excel_file = path 
    wb = load_workbook(excel_file, data_only = True)
    sh = wb[wb.sheetnames[0]]
    df = pd.read_excel(excel_file,
                    sheet_name=wb.sheetnames[0],
                    usecols='A:D',skiprows=[1])
    
    df = df[df['Comments'].notnull()]
    color = []
    cycle = []
    for i in df.index:
        hex = sh['A'+str(i+3)].fill.start_color.index # this gives you Hexadecimal value of the color
        cycle.append(calendar_tag.split()[-1])
        if hex == 'FF00FF00':
            color.append('green')
        elif hex == 'FFFFFF00':
            color.append('yellow')
        elif hex == 'FFFF9900':
            color.append('orange')
    df['Twitter'] = df['Twitter'].apply(make_clickable)
    df['Color'] = color
    df['Cycle'] = cycle
    df['Comments'] = df['Comments'].str.replace("\n\n","").str.replace("\n \n","")
    df['Mint Date'] = df['Mint Date'].astype(str)
    return df