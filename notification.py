import smtplib
from email.message import EmailMessage

# Configuration
smtp_server = "smtp.gmail.com"
port = 465  # Port for SSL
sender_email = "mercia.jeno@gmail.com"
password = "mwhr iifo cjvz inyw"  # 16-digit App Password
receiver_email = "mercia.jeno@gmailcom"

# Create the message
msg = EmailMessage()
msg['Subject'] = "Testing Python Email"
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content("Hello! This message was sent using Python's smtplib.")

# Send the email
with smtplib.SMTP_SSL(smtp_server, port) as server:
    server.login(sender_email, password)
    server.send_message(msg)
    print("Email sent successfully!")
