import json
import os
from dotenv import load_dotenv
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def connect_to_google_sheets(sheet_name):
    try:
        # Carregar credenciais da variável de ambiente
        sheet_name = os.getenv('PLANILHA_DINDINZ')
        credentials_info = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON', '{}'))
        credentials = Credentials.from_service_account_info(
            credentials_info,
            scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
        )
        
        # Autorizar o cliente gspread
        client = gspread.authorize(credentials)
        
        # Abrir a planilha especificada
        sheet = client.open(sheet_name).sheet1  # Abrir a primeira folha da planilha
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Planilha '{sheet_name}' não encontrada. Verifique o nome e tente novamente.")
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        return None

def save_data_to_sheet(sheet, data):
    try:
        sheet.append_row(data)
        st.success("Dados salvos com sucesso no Google Sheets!")
    except Exception as e:
        st.error(f"Erro ao salvar dados no Google Sheets: {e}")

# Defina a função google_sheets_interface se ela for necessária
def google_sheets_interface():
    st.title("Integração com Google Sheets")
    
    sheet_name = st.text_input("Nome da Planilha no Google Sheets")
    if st.button("Conectar"):
        sheet = connect_to_google_sheets(sheet_name)
        if sheet:
            st.success("Conectado com sucesso!")
            st.write(sheet.get_all_records())  # Exibir todos os registros como exemploimport json
