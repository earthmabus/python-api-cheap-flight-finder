import os
import smtplib

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

class NotificationManager:
    def __init__(self):
        self.m_myemail = GMAIL_ADDRESS
        self.m_password = GMAIL_PASSWORD

    def send_email(self, to_address, subject, message):
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(self.m_myemail, self.m_password)
                connection.sendmail(from_addr=self.m_myemail, to_addrs=to_address, msg=f"Subject: {subject}\n\n{message}")
                print("Successfully sent email")
        except Exception as e:
            print(f"Encountered exception while sending email: {e}")
