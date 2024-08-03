# src/database.py

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Configuração das credenciais do Google Sheets
def get_gsheet_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes
    )
    client = gspread.authorize(credentials)
    return client

def get_data(sheet_name):
    client = get_gsheet_client()
    sheet = client.open("MeuDinDinz").worksheet(sheet_name)
    data = pd.DataFrame(sheet.get_all_records())
    return data

def update_data(sheet_name, data):
    client = get_gsheet_client()
    sheet = client.open("MeuDinDinz").worksheet(sheet_name)
    sheet.clear()
    sheet.update([data.columns.values.tolist()] + data.values.tolist())