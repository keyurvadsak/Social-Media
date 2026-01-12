import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.schemas.email import Email_Send
from app.config.config import settings

def send_email(email:Email_Send):
    try:
        msg = MIMEText(email.body, "html")
        msg["to"] = email.to_email
        msg["subject"] = email.subject
        msg["from"] = settings.mail_from
        
        
        server = smtplib.SMTP(settings.mail_server, settings.mail_port)
        server.starttls()
        server.login(settings.mail_username,settings.mail_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False
    
    
