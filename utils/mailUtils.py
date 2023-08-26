from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import utils.DbUtils as DbUtils
import smtplib
import ssl
import os


class Mail:
    def __init__(self, receiver_email):
        load_dotenv()
        self.smtp_server = os.getenv("SMTP_HOST")
        self.smtp_port = os.getenv("SMTP_PORT")
        self.smtp_email = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.receiver_email = receiver_email
        self.secret_key = os.getenv("DB_KEY")
        self.token_id = None
        self.user_id = None

    def addToDatabase(self):
        db = DbUtils.DataBase()
        self.user_id, self.token_id, user = db.createUser()
        return user

    def sendMail(self):
        isAdded = self.addToDatabase()

        #create a email
        message = MIMEMultipart("alternative")
        message["Subject"] = "[RiasCloud] Access to the API (Reddit Token)"
        message["From"] = self.smtp_email
        message["To"] = self.receiver_email
        # Create the plain-text and HTML version of your message
        text = f"""\
        Dear {self.receiver_email},
        
        We're excited to provide you with access to Service Reddit API. Here are the details you'll need to get started:
        
        Token_id: {self.token_id}
        user_id: {self.user_id}
        
        Please keep this information safe and do not share it with anyone. These credentials will allow you to log in to the service and access all its features.
        
        For detailed instructions on how to use the service, please refer to our online documentation at the following link: [API Documentations](https://api.riascloud.fr/docs).
        
        If you have any questions or issues, feel free to reach out to us at [
        ]. We're here to assist you.
        
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

        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        #print("SMTP Server Connected")
        server.login(self.smtp_email, self.smtp_password)
        #print("Login Successful")
        if isAdded == "User Added":
            server.sendmail(self.smtp_email, self.receiver_email, message.as_string())
            #print("Email sent!")
        server.quit()


if __name__ == '__main__':
    load_dotenv()
    mail = Mail(receiver_email="test.dev@riascloud.fr")
    mail.sendMail()