from dotenv import load_dotenv
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import smtplib
    import ssl
    import os

load_dotenv()
smtp_server = "mail.riascloud.fr"
port = 465 # For SSL
sender_email = "no-reply@riascloud.fr"  # Enter your address
receiver_email = "testfonction.dev@riascloud.fr"  # Enter receiver address
test="RAndom"
#create a email
message = MIMEMultipart("alternative")
message["Subject"] = "[RiasCloud] Access to the API (Reddit Token)"
message["From"] = sender_email
message["To"] = receiver_email
# Create the plain-text and HTML version of your message
text = f"""\
Dear {receiver_email},

We're excited to provide you with access to Service XYZ. Here are the details you'll need to get started:

Token_id: [Your_token_id]
user_id: [Your_user_id]

Please keep this information safe and do not share it with anyone. These credentials will allow you to log in to the service and access all its features.

For detailed instructions on how to use the service, please refer to our online documentation at the following link: [API Documentations](https://api.riascloud.fr/docs).

If you have any questions or issues, feel free to reach out to us at [your@email.com]. We're here to assist you.

Best regards,
RiasCloud Team
"""
# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)

# Create a secure SSL context
context = ssl.create_default_context()

server = smtplib.SMTP_SSL(smtp_server, port)
print("SMTP Server Connected")
server.login(sender_email, os.getenv("SMTP_PASSWORD"))
print("Login Successful")
server.sendmail(sender_email, receiver_email, message.as_string())
print("Email sent!")
server.quit()