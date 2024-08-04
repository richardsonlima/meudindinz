import gspread
from google.oauth2.service_account import Credentials
import os
import json

def connect_to_google_sheets(sheet_name):
    try:
        # Obter o JSON de credenciais da variável de ambiente
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")

        if not creds_json:
            raise ValueError("A variável de ambiente 'GOOGLE_SHEETS_CREDENTIALS_JSON' não está definida.")

        # Carregar as credenciais do JSON
        creds_info = json.loads(creds_json)

        # Autenticação com credenciais
        creds = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/spreadsheets"])

        # Autenticando com gspread
        client = gspread.authorize(creds)

        # Acessar a planilha
        spreadsheet = client.open(sheet_name)

        # Selecionar uma aba
        sheet = spreadsheet.sheet1

        # Ler todos os dados
        data = sheet.get_all_records()

        return data

    except gspread.exceptions.SpreadsheetNotFound:
        raise FileNotFoundError(f"Planilha '{sheet_name}' não encontrada. Verifique o nome da planilha.")
    except gspread.exceptions.APIError as api_err:
        raise ConnectionError(f"Erro ao acessar a API do Google Sheets: {api_err}")
    except Exception as e:
        raise RuntimeError(f"Erro ao conectar ao Google Sheets: {e}")
