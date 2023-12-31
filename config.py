import json
import os 

if os.path.exists('.secrets'):
    with open('.secrets','r') as f:
        secrets = json.loads(f.read())
else:
    import streamlit as st
    secrets = st.secrets

NOTION_API_KEY = secrets['NOTION']['NOTION_API_KEY']
NOTION_DB_ID = secrets['NOTION']['NOTION_DB_ID']

GOOGLE_API_CREDS = secrets['GOOGLE']['GOOGLE_API_CREDS']
GOOGLE_SPREADSHEET_KEY = secrets['GOOGLE']['GOOGLE_SPREADSHEET_KEY']

ADILKHAN_PDF_FOLDER_ID = secrets['GOOGLE']['GOOGLE_PDF_FOLDER_IDS']["ADILKHAN_PDF_FOLDER_ID"]
BALZHAN_PDF_FOLDER_ID = secrets['GOOGLE']['GOOGLE_PDF_FOLDER_IDS']["BALZHAN_PDF_FOLDER_ID"]

PDF_FOLDER_ID_LIST = [
            ('Adilkhan', ADILKHAN_PDF_FOLDER_ID),
            ('Balzhan', BALZHAN_PDF_FOLDER_ID)
        ]