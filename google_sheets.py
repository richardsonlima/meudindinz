import gspread
from google.oauth2.service_account import Credentials
import os
import json
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO)

def connect_to_google_sheets(sheet_name):
    try:
        logging.info("Iniciando a conexão com o Google Sheets...")

        # Obter o JSON de credenciais da variável de ambiente
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
        if not creds_json:
            raise ValueError("A variável de ambiente 'GOOGLE_SHEETS_CREDENTIALS_JSON' não está definida.")
        
        logging.info("Credenciais JSON obtidas com sucesso.")
        
        # Carregar as credenciais do JSON
        creds_info = json.loads(creds_json)
        logging.info("Credenciais JSON carregadas e analisadas.")
        
        # Autenticação com credenciais
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]  # Certifique-se de que este escopo está correto
        )
        
        logging.info("Credenciais de autenticação configuradas.")
        
        # Autenticando com gspread
        client = gspread.authorize(creds)
        
        logging.info("Autenticado com sucesso no Google Sheets.")
        
        # Acessar a planilha
        spreadsheet = client.open(sheet_name)
        logging.info(f"Acesso à planilha '{sheet_name}' concluído.")
        
        # Selecionar uma aba
        sheet = spreadsheet.sheet1
        
        # Ler todos os dados
        data = sheet.get_all_records()
        
        logging.info(f"Dados da planilha '{sheet_name}' carregados com sucesso.")
        return data

    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Planilha '{sheet_name}' não encontrada. Verifique o nome da planilha.")
        raise FileNotFoundError(f"Planilha '{sheet_name}' não encontrada. Verifique o nome da planilha.")
    except gspread.exceptions.APIError as api_err:
        logging.error(f"Erro ao acessar a API do Google Sheets: {api_err}")
        raise ConnectionError(f"Erro ao acessar a API do Google Sheets: {api_err}")
    except Exception as e:
        logging.error(f"Erro ao conectar ao Google Sheets: {e}")
        raise RuntimeError(f"Erro ao conectar ao Google Sheets: {e}")

def save_data_to_sheet(sheet_name, data):
    try:
        logging.info("Iniciando o salvamento de dados no Google Sheets...")

        # Obter o JSON de credenciais da variável de ambiente
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
        if not creds_json:
            raise ValueError("A variável de ambiente 'GOOGLE_SHEETS_CREDENTIALS_JSON' não está definida.")
        
        logging.info("Credenciais JSON obtidas com sucesso.")

        # Carregar as credenciais do JSON
        creds_info = json.loads(creds_json)
        logging.info("Credenciais JSON carregadas e analisadas.")
        
        # Autenticação com credenciais
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]  # Certifique-se de que este escopo está correto
        )
        
        logging.info("Credenciais de autenticação configuradas.")
        
        # Autenticando com gspread
        client = gspread.authorize(creds)
        
        logging.info("Autenticado com sucesso no Google Sheets.")
        
        # Acessar a planilha
        spreadsheet = client.open(sheet_name)
        logging.info(f"Acesso à planilha '{sheet_name}' concluído.")

        # Selecionar uma aba
        sheet = spreadsheet.sheet1
        
        # Limpar os dados existentes na planilha
        sheet.clear()
        logging.info(f"Dados anteriores na planilha '{sheet_name}' foram apagados.")
        
        # Atualizar a planilha com novos dados
        sheet.update([data[0].keys()] + [list(item.values()) for item in data])
        logging.info(f"Novos dados foram salvos com sucesso na planilha '{sheet_name}'.")
        
        return True

    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Planilha '{sheet_name}' não encontrada. Verifique o nome da planilha.")
        raise FileNotFoundError(f"Planilha '{sheet_name}' não encontrada. Verifique o nome da planilha.")
    except gspread.exceptions.APIError as api_err:
        logging.error(f"Erro ao acessar a API do Google Sheets: {api_err}")
        raise ConnectionError(f"Erro ao acessar a API do Google Sheets: {api_err}")
    except Exception as e:
        logging.error(f"Erro ao salvar dados no Google Sheets: {e}")
        raise RuntimeError(f"Erro ao salvar dados no Google Sheets: {e}")