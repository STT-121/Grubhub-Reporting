import os
from email_client import EmailClient
from report_generator import ReportGenerator
from sheets import GoogleSheetsHandler
from dotenv import load_dotenv

load_dotenv()

# Example usage
if __name__ == "__main__":
    creds_file = "service_account.json"
    sheet_name = "GH Sample Data"

    # Initialize Google Sheets handler
    gsheet_handler = GoogleSheetsHandler(creds_file, sheet_name)
    supervisors_df = gsheet_handler.fetch_data_from_tab('Supervisors')
    employees_df = gsheet_handler.fetch_data_from_tab('Employees')
    orders_df = gsheet_handler.fetch_data_from_tab('Orders')

    # Initialize email client
    email_client = EmailClient(smtp_server=os.getenv('SMTP_SERVER'), smtp_port=os.getenv('SMTP_PORT'),
                               username=os.getenv('SENDER_EMAIL'), password=os.getenv('SMTP_PASSWORD'))

    # Initialize the report generator
    report_generator = ReportGenerator(orders_df, employees_df, supervisors_df,email_client)
    report_generator.generate_supervisor_reports()
    report_generator.generate_employee_reports()
