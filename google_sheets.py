import gspread
from google.oauth2.service_account import Credentials
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

sheet_name = "meu_dindinz_planilha"  # Substitua "nome_da_sua_planilha" pelo nome real da sua planilha

def connect_to_google_sheets(sheet_name):
    try:
        logging.info("Starting connection to Google Sheets...")
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
        if not creds_json:
            raise ValueError("Environment variable 'GOOGLE_SHEETS_CREDENTIALS_JSON' is not set.")
        
        logging.info("JSON credentials obtained successfully.")
        
        creds_info = json.loads(creds_json)
        logging.info("JSON credentials loaded and parsed.")
        
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        
        logging.info("Authentication credentials configured.")
        
        client = gspread.authorize(creds)
        
        logging.info("Successfully authenticated with Google Sheets.")
        
        spreadsheet = client.open(sheet_name)
        logging.info(f"Access to spreadsheet '{sheet_name}' completed.")
        
        sheet = spreadsheet.sheet1
        
        data = sheet.get_all_records()
        
        logging.info(f"Data from spreadsheet '{sheet_name}' loaded successfully.")
        return data

    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Spreadsheet '{sheet_name}' not found.")
        raise FileNotFoundError(f"Spreadsheet '{sheet_name}' not found.")
    except gspread.exceptions.APIError as api_err:
        logging.error(f"Error accessing Google Sheets API: {api_err}")
        raise ConnectionError(f"Error accessing Google Sheets API: {api_err}")
    except Exception as e:
        logging.error(f"Error connecting to Google Sheets: {e}")
        raise RuntimeError(f"Error connecting to Google Sheets: {e}")

def save_data_to_sheet(sheet_name, data):
    try:
        logging.info("Starting to save data to Google Sheets...")

        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
        if not creds_json:
            raise ValueError("Environment variable 'GOOGLE_SHEETS_CREDENTIALS_JSON' is not set.")
        
        logging.info("JSON credentials obtained successfully.")

        creds_info = json.loads(creds_json)
        logging.info("JSON credentials loaded and parsed.")
        
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        
        logging.info("Authentication credentials configured.")
        
        client = gspread.authorize(creds)
        
        logging.info("Successfully authenticated with Google Sheets.")
        
        spreadsheet = client.open(sheet_name)
        logging.info(f"Access to spreadsheet '{sheet_name}' completed.")

        sheet = spreadsheet.sheet1
        
        # Clear existing data
        sheet.clear()
        logging.info(f"Previous data in spreadsheet '{sheet_name}' has been cleared.")
        
        # Convert data to a list of lists if it isn't already
        if isinstance(data, list):
            # If data is a list of dictionaries, convert to list of lists
            if isinstance(data[0], dict):
                data = [list(data[0].keys())] + [list(item.values()) for item in data]
            # If data is already a list of lists, no need to convert
            elif isinstance(data[0], list):
                pass
            else:
                raise ValueError("Data is neither a list of dictionaries nor a list of lists.")
        else:
            raise ValueError("Data should be a list.")

        sheet.update(data)
        logging.info(f"New data successfully saved to spreadsheet '{sheet_name}'.")

        return True

    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Spreadsheet '{sheet_name}' not found.")
        raise FileNotFoundError(f"Spreadsheet '{sheet_name}' not found.")
    except gspread.exceptions.APIError as api_err:
        logging.error(f"Error accessing Google Sheets API: {api_err}")
        raise ConnectionError(f"Error accessing Google Sheets API: {api_err}")
    except Exception as e:
        logging.error(f"Error saving data to Google Sheets: {e}")
        raise RuntimeError(f"Error saving data to Google Sheets: {e}")