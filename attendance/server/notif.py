from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Validate environment variables
if not EMAIL or not PASSWORD:
    raise ValueError("EMAIL and PASSWORD must be set in your .env file")


def send_mail(
    target: str,
    subject: str = "Borrowed Book Notification",
    body: str = "You have borrowed a book. Please return it on time.",
) -> None:
    """
    Sends an email to the target address with the given subject and body.
    """
    if not EMAIL or not PASSWORD:
        raise ValueError("EMAIL and PASSWORD must be set in your .env file")
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = target
    msg.set_content(body)

    # Use 'with' to ensure connection is properly closed
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(EMAIL, PASSWORD)
            mail.send_message(msg)
    except smtplib.SMTPException as e:
        # Proper error handling
        print(f"Failed to send email to {target}: {e}")
