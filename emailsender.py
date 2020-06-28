import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import configparser
from datetime import datetime

class EmailSender:

    credentials  = 'credentials'
    passwordStr  = 'password'
    smtpStr      = "smtp"
    portStr      = "port"
    senderStr    = "sender"

    target       = "target"
    recipientStr = "recipient"
    subjectStr   = "subject"

    """
    """
    def __init__(self, filename):
        config = self.getEmailConfig(filename)
        self.password = config.get(self.credentials, self.passwordStr)
        self.smtp = config.get(self.credentials, self.smtpStr)
        self.port = config.get(self.credentials, self.portStr)
        self.sender = config.get(self.credentials, self.senderStr)

        self.recipient = config.get(self.target, self.recipientStr)
        self.subject = config.get(self.target, self.subjectStr)

    """
    """
    def getEmailConfig(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config


    """
    """
    def sendEmail(self, termins):
        # Create e-mail message
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = self.recipient
        msg["Subject"] = self.subject

        body = "<html><head></head><body><h2>Termins available at {}:</h2><br><br> {}".format(datetime.now(), termins) + "</body></html>"
        msg.attach(MIMEText(body, "html"))


        context = ssl.create_default_context()

        # Send message
        smtp = smtplib.SMTP(self.smtp, self.port)
        smtp.ehlo()
        smtp.starttls(context = context)
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.recipient, msg.as_string())
        smtp.quit()
        print("-> Email sent")