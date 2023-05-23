from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib, os

load_dotenv('.env')

def send_mail(subject:str, message:str, to_email:str) -> bool:
    sender = os.environ.get('smtp_email')
    password = os.environ.get('smtp_password')

    server = smtplib.SMTP('smtp.yandex.ru', 587)
    server.starttls()
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email

    try:
        server.login(sender, password)
        server.send_message(msg)
        return True 
    except Exception as error:
        return f"Error: {error}"
print(send_mail('SMTP PYTHON', 'Testing smtp sender from Python', 'toshaxar@mail.ru'))

# emails = ['ktoktorov144@gmail.com', 'toktorovkurmanbek92@gmail.com', 'ashatkydyrov433@gmail.com', 'toktoroveldos15@gmail.com']