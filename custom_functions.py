import pdb

import pandas as pd


def split_employee_data(df, column_name):
    """
    Split the employee name and email from the given column in the DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing employee data in a single column.
    column_name (str): The name of the column that contains the employee data.

    Returns:
    pd.DataFrame: DataFrame with two new columns 'Employee Name' and 'Email'.
    """
    # Lists to store names and emails
    names = []
    emails = []
    supervisor_name = []
    supervisor_email = []
    # Iterate through each row in the DataFrame column
    # pdb.set_trace()



    for index, entry in df.iterrows():
        # Split by comma to get individual name-email pairs
        pairs = entry[column_name].split(',')

        for pair in pairs:
            # Split the name and email by the opening bracket '('
            name, email = pair.split('(')
            name = name.strip()  # Remove extra spaces around the name
            email = email.replace(')', '').strip()  # Remove the closing bracket and any extra spaces
            names.append(name)
            emails.append(email)
            supervisor_name.append(entry['Supervisor Name'])
            supervisor_email.append(entry['Supervisor Email'])
    emp_df = pd.DataFrame()
    emp_df['Employee Name']=names
    emp_df['Employee Email']= emails
    emp_df['Supervisor Name']= supervisor_name
    emp_df['Supervisor Email']= supervisor_email

    return emp_df


def group_by_supervisor(df, supervisor_name_col, supervisor_email_col):
    """
    Group records based on supervisor name and email address.

    Parameters:
    df (pd.DataFrame): DataFrame containing supervisor data.
    supervisor_name_col (str): The name of the column with supervisor names.
    supervisor_email_col (str): The name of the column with supervisor emails.

    Returns:
    pd.DataFrameGroupBy: A DataFrameGroupBy object grouped by supervisor name and email.
    """
    # Group by both supervisor name and supervisor email
    grouped_df = df.groupby([supervisor_name_col, supervisor_email_col])
    return grouped_df
