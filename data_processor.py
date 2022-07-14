import pandas as pd
from datetime import datetime
# ---- HYPERLINK ----
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[0]
    return f'<a target="_blank" href="{link}">{text}</a>'

def custom_sort(df):
    df_mapping = pd.DataFrame({
    'status': ['Green', 'Orange', 'Yellow', 'Not Good Enough','Other','Re-Review Needed','Non Ethereum'],
    })
    sort_mapping = df_mapping.reset_index().set_index('status')
    df['status_num'] = df['Status'].map(sort_mapping['index'])
    return df

# ---- READ EXCEL ----
def load_data():
    sheet_id = "1HLWkNCVi3mggBYVZNdHooP8KwTw47F7ATrmfKmvK6GY"
    gid = "1619771889"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    df = pd.read_excel(url)
    df = df[['Project','Mint Date','Twitter','Status','Description','Date Last Reviewed']]
    df['Twitter'] = df['Twitter'].apply(make_clickable)
    df['Date Last Reviewed'] = df['Date Last Reviewed'].dt.strftime('%m/%d/%Y')
    df = df[df['Date Last Reviewed'].notna()]
    df = df[df['Status'].notna()]
    df = df[df['Project'].notna()]
    df = df[df['Status'] != 'Already Minted']
    df.loc[df["Status"] == "Green",'Project'] = "<a style='color:green;'>" + df.loc[df["Status"] == "Green",'Project'] + "</a>"
    df.loc[df["Status"] == "Orange",'Project'] = "<a style='color:orange;'>" + df.loc[df["Status"] == "Orange",'Project'] + "</a>"
    df.loc[df["Status"] == "Yellow",'Project'] = "<a style='color:yellow;'>" + df.loc[df["Status"] == "Yellow",'Project'] + "</a>"
    df = custom_sort(df)
    df.rename(columns = {'Date Last Reviewed':'Cycle'}, inplace = True)
    df["Mint Date"] = df['Mint Date'].apply(lambda x: pd.to_datetime(x).strftime('%m/%d/%Y') if type(x) is datetime else x)
    pd.set_option('display.colheader_justify', 'left')
    return df.fillna(' ')

#df = load_data()
#print(df)