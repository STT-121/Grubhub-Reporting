import gspread
import pandas as pd
from google.oauth2.service_account import Credentials



class GoogleSheetsHandler:
    def __init__(self, creds_file, sheet_name):
        # Authenticate and connect to Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        self.creds = Credentials.from_service_account_file(creds_file, scopes=scope)
        self.client = gspread.authorize(self.creds)
        self.sheet_name = sheet_name

    def fetch_data_from_tab(self, tab_name):
        # Open the tab by its name
        sheet = self.client.open(self.sheet_name).worksheet(tab_name)
        # Fetch the data into a pandas DataFrame
        data = sheet.get_all_records()
        return pd.DataFrame(data)
