import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(message):
    # Email configuration
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    sender_email = 'sender@example.com'
    receiver_email = 'receiver@example.com'
    password = 'your_password'

    # Email content
    subject = 'Transaction Alert'
    body = message

    # Construct the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

