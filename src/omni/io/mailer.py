import re
import os
import smtplib
import ssl
from email.message import EmailMessage
import logging
from datetime import datetime


class Mailer:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")

    def validate_mail(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def send_mail(self, recipient: str, body: str, sender: str = None) -> bool:
        if not self.validate_mail(recipient):
            logging.error(f"Invalid recipient email: {recipient}")
            return False

        sender = sender or self.username

        message = EmailMessage()
        message["From"] = sender
        message["To"] = recipient
        today = datetime.now()
        subject_value = f"Omni: News Report - {today.strftime('%A (%d %B %y)')}"
        message["Subject"] = subject_value
        message.set_content(body)

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.username, self.password)
                server.send_message(message)
            logging.info(f"Email successfully sent to {recipient}")
            return True
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return False


# Example usage
if __name__ == "__main__":
    mailer = Mailer()
    success = mailer.send_mail(recipient="navaneethan.ghanti@gmil.com",
                               body="This is a test email from Mailer class.")
