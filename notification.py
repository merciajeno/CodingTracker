import smtplib
from email.message import EmailMessage
from tracker import submit_streaks
from tracker import submit_leetcode_commits
# Configuration
smtp_server = "smtp.gmail.com"
port = 465  # Port for SSL
sender_email = "mercia.jeno@gmail.com"
password = "mwhr iifo cjvz inyw"  # 16-digit App Password
receiver_email = "mercia.jeno@gmail.com"

# Create the message
msg = EmailMessage()
msg['Subject'] = "Testing Python Email"
msg['From'] = sender_email
msg['To'] = receiver_email
message=f'The streak is {submit_streaks()}. The leetcode commits is:{submit_leetcode_commits()}'
msg.set_content(message)

# Send the email
with smtplib.SMTP_SSL(smtp_server, port) as server:
    server.login(sender_email, password)
    server.send_message(msg)
    print("Email sent successfully!")
