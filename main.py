import os
import pandas as pd
from dotenv import load_dotenv
from google_sheets import GoogleSheetManager
from custom_functions import split_employee_data, group_by_supervisor

import pdb

load_dotenv()
# Example usage
if __name__ == "__main__":
    creds_file = "service_account.json"
    g_sheet = GoogleSheetManager(creds_file)

    # manage  mapping
    mapping = g_sheet.get_sheet_and_tab_by_name('GH Sample Data', os.getenv('MAPPING_SHEET'))
    mapping_df = pd.DataFrame(mapping.get_all_records())

    # manage employee
    employees_df = split_employee_data(mapping_df, 'Direct Reports')

    # manage supervisor
    supervisor_data_df = group_by_supervisor(employees_df, 'Supervisor Name', 'Supervisor Email')

    # Employee Wise Sheet Creation:
    for index, entry in employees_df.iterrows():
        print(f"{index} - {entry['Employee Name']}  ,{entry['Employee Email']}")
        ret_sheet, sheet_exists = g_sheet.duplicate_sheet(os.getenv('EMPLOYEE_TEMPLATE'),
                                                          entry['Employee Name'])
        g_sheet.update_cell_in_tab(ret_sheet, 'Orders', 'B1', [[entry['Employee Email']]])
        if sheet_exists:
            # g_sheet.share_sheet(ret_sheet.get('id'), entry['Employee Email'],)
            g_sheet.share_sheet(ret_sheet, 'syedtaymoor121@gmail.com', 'writer')

    # Super Wise Sheet Creation:
    for (supervisor_name, supervisor_email), group in supervisor_data_df:
        print(f"Supervisor: {supervisor_name}, {supervisor_email}")
        ret_sheet, sheet_exists = g_sheet.duplicate_sheet(os.getenv('SUPERVISOR_TEMPLATE'),
                                                          supervisor_name if supervisor_name else supervisor_email)
        g_sheet.update_cell_in_tab(ret_sheet, 'Orders', 'B1',
                                   [group.get('Employee Email').tolist()])
        if sheet_exists:
            # g_sheet.share_sheet(ret_sheet, '', 'writer')
            g_sheet.share_sheet(ret_sheet.get('id'), supervisor_email, )
