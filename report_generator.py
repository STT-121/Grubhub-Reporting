import pandas as pd

class ReportGenerator:
    def __init__(self, orders_df, employees_df, supervisors_df,Email_client):
        self.orders_df = orders_df
        self.employees_df = employees_df
        self.supervisors_df = supervisors_df
        self.email_client = Email_client

    def generate_supervisor_reports(self):
        self.orders_df['Employee Name'] = self.orders_df['AllocatedFirstName'] + ' ' + self.orders_df[
            'AllocatedLastName']
        self.orders_df = self.orders_df.merge(
            self.employees_df[['Employee Email', 'Employee Name', 'Supervisor Email']],
            left_on='Employee Name', right_on='Employee Name', how='left')
        self.orders_df = self.orders_df.merge(self.supervisors_df[['Supervisor Email', 'Supervisor Name']],
                                              left_on='Supervisor Email', right_on='Supervisor Email', how='left')

        for supervisor_email, supervisor_df in self.orders_df.groupby('Supervisor Email'):
            supervisor_name = supervisor_df['Supervisor Name'].iloc[0]
            html_content = self._generate_supervisor_report_html(supervisor_df)
            self.email_client.send_email('syedtaymoor.handsome@gmail.com',
                                         f"Order Report for Supervisor: {supervisor_name}",
                                         html_content)
            print(f"Report sent to supervisor {supervisor_name} with email {supervisor_email}")

    def _generate_supervisor_report_html(self, supervisor_df):
        supervisor_name = supervisor_df['Supervisor Name'].iloc[0]

        html = '<html><head><style>'
        html += 'body { font-family: Arial, sans-serif; }'
        html += 'h2 { color: #2a7f62; }'
        html += 'table { border-collapse: collapse; width: 100%; margin: 20px 0; }'
        html += 'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }'
        html += 'th { background-color: #4CAF50; color: white; }'
        html += 'tr:nth-child(even) { background-color: #f2f2f2; }'
        html += 'tr.total-row { background-color: #f4a460; font-weight: bold; }'
        html += 'tr.employee-header { background-color: #ffebcd; font-weight: bold; }'
        html += '</style></head><body>'
        html += f"<h2>Order Report for Supervisor: {supervisor_name}</h2>"

        month_totals = {}
        vendor_totals = {}
        employee_totals = {}
        overall_total = 0

        html += '<table>'
        html += '<thead><tr>'
        html += '<th>Employee Name</th>'
        html += '<th>Vendor Name</th>'
        html += '<th>Delivery Month</th>'
        html += '<th>Grand Total</th>'
        html += '</tr></thead>'
        html += '<tbody>'

        for employee_name, employee_orders in supervisor_df.groupby('Employee Name'):
            employee_total = 0
            html += f'<tr class="employee-header"><td colspan="4">{employee_name}</td></tr>'

            for _, row in employee_orders.iterrows():
                vendor_name = row['VendorName']
                delivery_month = pd.to_datetime(row['DeliveryDate']).strftime('%B')
                grand_total = row['Grand_Total']

                employee_total += grand_total
                month_totals[delivery_month] = month_totals.get(delivery_month, 0) + grand_total
                vendor_totals[vendor_name] = vendor_totals.get(vendor_name, 0) + grand_total
                overall_total += grand_total

                html += '<tr>'
                html += f'<td></td>'
                html += f'<td>{vendor_name}</td>'
                html += f'<td>{delivery_month}</td>'
                html += f'<td>{grand_total:.2f}</td>'
                html += '</tr>'

            html += '<tr class="total-row">'
            html += f'<td><strong>Total</strong></td>'
            html += '<td></td>'
            html += '<td></td>'
            html += f'<td>{employee_total:.2f}</td>'
            html += '</tr>'

        html += '<tr class="total-row">'
        html += '<td><strong>Overall Total</strong></td>'
        html += '<td></td>'
        html += '<td></td>'
        html += f'<td>{overall_total:.2f}</td>'
        html += '</tr>'

        html += '</tbody></table>'
        html += '</body></html>'

        return html

    def generate_employee_reports(self):
        for employee_name, employee_orders in self.orders_df.groupby('Employee Name'):
            employee_total = employee_orders['Grand_Total'].sum()
            if employee_total > 0:
                employee_email = employee_orders['Employee Email'].iloc[0]
                html_content = self._generate_employee_report_html(employee_name, employee_orders)
                self.email_client.send_email('syedtaymoor.handsome@gmail.com',
                                             f"Order Report for Employee : {employee_name}",
                                             html_content)
                print(f"Report sent to employee {employee_name} with email {employee_email}")

    def _generate_employee_report_html(self, employee_name, employee_orders):
        html = '<html><head><style>'
        html += 'body { font-family: Arial, sans-serif; }'
        html += 'h2 { color: #2a7f62; }'
        html += 'table { border-collapse: collapse; width: 100%; margin: 20px 0; }'
        html += 'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }'
        html += 'th { background-color: #4CAF50; color: white; }'
        html += 'tr:nth-child(even) { background-color: #f2f2f2; }'
        html += 'tr.total-row { background-color: #f4a460; font-weight: bold; }'
        html += '</style></head><body>'
        html += f"<h2>Order Report for Employee: {employee_name}</h2>"

        html += '<table>'
        html += '<thead><tr>'
        html += '<th>Vendor Name</th>'
        html += '<th>Delivery Month</th>'
        html += '<th>Grand Total</th>'
        html += '</tr></thead>'
        html += '<tbody>'

        for _, row in employee_orders.iterrows():
            vendor_name = row['VendorName']
            delivery_month = pd.to_datetime(row['DeliveryDate']).strftime('%B')
            grand_total = row['Grand_Total']

            html += '<tr>'
            html += f'<td>{vendor_name}</td>'
            html += f'<td>{delivery_month}</td>'
            html += f'<td>{grand_total:.2f}</td>'
            html += '</tr>'

        html += '<tr class="total-row">'
        html += '<td><strong>Total</strong></td>'
        html += '<td></td>'
        html += f'<td>{employee_orders["Grand_Total"].sum():.2f}</td>'
        html += '</tr>'

        html += '</tbody></table>'
        html += '</body></html>'

        return html
