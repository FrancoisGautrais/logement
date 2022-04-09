# from website.models.settings import settings
import smtplib, ssl
settings={}

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(sender, reciever, message, opts=None):
    opts = opts or {}
    smtp = opts.get("smtp", settings.get("mail.smtp"))
    _tmp = smtp.split(":")
    smtp_host = _tmp[0]
    smtp_port = int(_tmp[1])


    user = opts.get("username", settings.get("mail.username"))
    email = opts.get("email", settings.get("mail.email"))
    password = opts.get("password",settings.get("mail.password"))
    headers = opts.get("headers", {})

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(user, password)
        msg = MIMEMultipart("alternative")
        for k, v in headers.items():
            msg[k] = v
        part1 = MIMEText(message)
        msg.attach(part1)
        server.sendmail(sender, reciever, msg.as_string().encode('ascii'))

def send_auto_email(name, addr, message, opts=None):
    content=f"""Message auto de {name} ({addr}).
=======================================
{message}
=======================================
"""
    dest = opts.get("email", settings.get("mail.email"))
    if not "headers" in opts: opts["headers"]={}
    opts["headers"]["Subject"]=f"Nouveau message de {name}"
    opts["headers"]["From"]=addr
    opts["headers"]["To"]=dest
    send_mail(dest, dest, content, opts)
