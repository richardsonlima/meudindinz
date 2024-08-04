import gspread
from google.oauth2.service_account import Credentials
import os
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def connect_to_google_sheets(sheet_name):
    try:
        logging.info("Starting connection to Google Sheets...")
        #sheet_name = os.getenv('PLANILHA_DINDINZ')
        sheet_name = 'meu_dindinz_planilha-v2'
        # Get credentials from environment variable
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
        if not creds_json:
            raise ValueError("Environment variable 'GOOGLE_SHEETS_CREDENTIALS_JSON' is not set.")
        
        logging.info("JSON credentials obtained successfully.")
        
        # Load credentials from JSON
        creds_info = json.loads(creds_json)
        logging.info("JSON credentials loaded and parsed.")
        
        # Authenticate with credentials
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        
        logging.info("Authentication credentials configured.")
        
        # Authenticate with gspread
        client = gspread.authorize(creds)
        
        logging.info("Successfully authenticated with Google Sheets.")
        
        # Access the spreadsheet
        spreadsheet = client.open(sheet_name)
        logging.info(f"Access to spreadsheet '{sheet_name}' completed.")
        
        # Select the first sheet
        sheet = spreadsheet.sheet1
        
        # Get all records
        data = sheet.get_all_records()
        
        logging.info(f"Data from spreadsheet '{sheet_name}' loaded successfully.")
        return data

    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Spreadsheet '{sheet_name}' not found. Please check the spreadsheet name.")
        raise FileNotFoundError(f"Spreadsheet '{sheet_name}' not found. Please check the spreadsheet name.")
    except gspread.exceptions.APIError as api_err:
        logging.error(f"Error accessing Google Sheets API: {api_err}")
        raise ConnectionError(f"Error accessing Google Sheets API: {api_err}")
    except Exception as e:
        logging.error(f"Error connecting to Google Sheets: {e}")
        raise RuntimeError(f"Error connecting to Google Sheets: {e}")

def save_data_to_sheet(sheet_name, data):
    try:
        logging.info("Starting to save data to Google Sheets...")

        # Get credentials from environment variable
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS_JSON")
        if not creds_json:
            raise ValueError("Environment variable 'GOOGLE_SHEETS_CREDENTIALS_JSON' is not set.")
        
        logging.info("JSON credentials obtained successfully.")

        # Load credentials from JSON
        creds_info = json.loads(creds_json)
        logging.info("JSON credentials loaded and parsed.")
        
        # Authenticate with credentials
        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        
        logging.info("Authentication credentials configured.")
        
        # Authenticate with gspread
        client = gspread.authorize(creds)
        
        logging.info("Successfully authenticated with Google Sheets.")
        
        # Access the spreadsheet
        spreadsheet = client.open(sheet_name)
        logging.info(f"Access to spreadsheet '{sheet_name}' completed.")

        # Select the first sheet
        sheet = spreadsheet.sheet1
        
        # Clear existing data
        sheet.clear()
        logging.info(f"Previous data in spreadsheet '{sheet_name}' has been cleared.")
        
        # Update the sheet with new data
        sheet.update([data[0].keys()] + [list(item.values()) for item in data])
        logging.info(f"New data successfully saved to spreadsheet '{sheet_name}'.")
        
        return True

    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Spreadsheet '{sheet_name}' not found. Please check the spreadsheet name.")
        raise FileNotFoundError(f"Spreadsheet '{sheet_name}' not found. Please check the spreadsheet name.")
    except gspread.exceptions.APIError as api_err:
        logging.error(f"Error accessing Google Sheets API: {api_err}")
        raise ConnectionError(f"Error accessing Google Sheets API: {api_err}")
    except Exception as e:
        logging.error(f"Error saving data to Google Sheets: {e}")
        raise RuntimeError(f"Error saving data to Google Sheets: {e}")

if __name__ == "__main__":
    # Example use case
    sheet_name = "Your_Spreadsheet_Name"
    data = connect_to_google_sheets(sheet_name)
    print(data)