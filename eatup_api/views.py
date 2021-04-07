from email.message import EmailMessage
import smtplib
import random
import string

def send_mail(receiver, subject, body="", html=""):
    sender = "apptestemail14@gmail.com"
    password = "MaeveNaeve@14"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    if html != "":
        msg.add_alternative(html, subtype="html")
    else:
        msg.set_content(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        
        smtp.login(sender, password)
        smtp.send_message(msg)

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str