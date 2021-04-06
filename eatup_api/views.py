from email.message import EmailMessage
import smtplib

def send_mail(receiver, subject, body="", html=None):
    sender = "apptestemail14@gmail.com"
    password = "MaeveNaeve@14"

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(body)
    if html != None:
        msg.add_alternative(html, subtype="html")

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender, password)
        smtp.send_message(msg)