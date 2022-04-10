# from website.models.settings import settings
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


def send_mail(sender, reciever, message, opts=None):
    opts = opts or {}
    smtp = opts.get("smtp")
    _tmp = smtp.split(":")
    smtp_host = _tmp[0]
    smtp_port = int(_tmp[1])


    user = opts.get("username")
    email = opts.get("email")
    password = opts.get("password")
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


def send_auto_email(dest, title, message, opts=None):
    opts = opts or settings.SMTP
    if not "headers" in opts: opts["headers"]={}
    opts["headers"]["Subject"]=title
    opts["headers"]["From"]=opts.get("email")
    opts["headers"]["To"]=dest
    send_mail(dest, dest, message, opts)
