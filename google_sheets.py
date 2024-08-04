import os
import json
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Função para conectar ao Google Sheets
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

# Função para salvar dados no Google Sheets
def save_data_to_sheet(sheet, data):
    try:
        sheet.append_row(data)
        st.success("Dados salvos com sucesso no Google Sheets!")
    except Exception as e:
        st.error(f"Erro ao salvar dados no Google Sheets: {e}")

