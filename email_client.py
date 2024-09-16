import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailClient:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(self, recipient_email, subject, html_content):
        try:
            # Create the email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = recipient_email

            # Attach the HTML content to the email
            part = MIMEText(html_content, 'html')
            msg.attach(part)

            # Send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, recipient_email, msg.as_string())

            print(f"Email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}. Error: {e}")
