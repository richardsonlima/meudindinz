import json
import os
import streamlit as st
from dotenv import load_dotenv
from google.oauth2 import service_account
import gspread

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

sheet_name = os.getenv('PLANILHA_DINDINZ')
# Access the secrets from the secrets.toml
service_account_info = st.secrets["google_service_account"]

# Create credentials object using service account info
credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)

# Use gspread to connect to Google Sheets
def connect_to_google_sheets(sheet_name):
    try:
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name).sheet1
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Planilha '{sheet_name}' não encontrada. Verifique o nome e tente novamente.")
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        return None

def google_sheets_interface():
    st.title("Integração com Google Sheets")
    
    sheet_name = st.text_input("Nome da Planilha no Google Sheets")
    if st.button("Conectar"):
        sheet = connect_to_google_sheets(sheet_name)
        if sheet:
            st.success("Conectado com sucesso!")
            st.write(sheet.get_all_records())

# Teste de conexão
if __name__ == "__main__":
    google_sheets_interface()
