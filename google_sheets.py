import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
import os

def google_sheets_interface():
    try:
        # Obter o JSON de credenciais da variável de ambiente
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")

        if not creds_json:
            st.error("Erro: Variável de ambiente 'GOOGLE_SHEETS_CREDENTIALS_JSON' não está definida.")
            return

        # Carregar as credenciais do JSON
        creds_info = json.loads(creds_json)

        # Autenticação com credenciais
        creds = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])

        # Autenticando com gspread
        client = gspread.authorize(creds)

        # Nome da planilha
        sheet_name = st.text_input("Nome da Planilha no Google Sheets", "Nome da Planilha")

        if not sheet_name:
            st.error("Erro: Por favor, insira o nome da planilha.")
            return

        # Acessar a planilha
        spreadsheet = client.open(sheet_name)

        # Selecionar uma aba
        sheet = spreadsheet.sheet1

        # Ler todos os dados
        data = sheet.get_all_records()

        # Exibir dados
        st.write(data)

    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Erro: Planilha '{sheet_name}' não encontrada. Verifique o nome da planilha.")
    except gspread.exceptions.APIError as api_err:
        st.error(f"Erro ao acessar a API do Google Sheets: {api_err}")
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")

# Executar a função de interface do Google Sheets
google_sheets_interface()