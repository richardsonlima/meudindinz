import streamlit as st
import os
import json
from dotenv import load_dotenv

from google.oauth2 import service_account
import gspread

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Acessando variáveis de ambiente
sheet_name = os.getenv('PLANILHA_DINDINZ')

google_credentials_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON']
google_credentials = json.loads(google_credentials_json)  # Parse JSON string to Python dict

# Criando as credenciais a partir do JSON
credentials = service_account.Credentials.from_service_account_info(google_credentials)

# Função para conectar ao Google Sheets
def connect_to_google_sheets(sheet_name):
    try:
        client = gspread.authorize(credentials)
        sheet = client.open(sheet_name).sheet1  # Abrir a primeira aba da planilha
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Planilha '{sheet_name}' não encontrada. Verifique o nome e tente novamente.")
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {e}")
        return None

def google_sheets_interface():
    st.title("Integração com Google Sheets")
    
    sheet_name = os.environ.get("PLANILHA_DINDINZ")  # Obtém o nome da planilha da variável de ambiente
    if st.button("Conectar"):
        sheet = connect_to_google_sheets(sheet_name)
        if sheet:
            st.success("Conectado com sucesso!")
            st.write(sheet.get_all_records())  # Exibir todos os registros como exemplo

# Teste de conexão
if __name__ == "__main__":
    google_sheets_interface()
