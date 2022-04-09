from django.http import HttpRequest
from django.conf import settings

def mail_notify(nb):
    data = { k:v  for k,v in settings.SMTP.items()}
    data["headers"]={
        "Subject" : f"{nb} nouveaux "
    }

def notify(req : HttpRequest, annocnes):
