from django.http import HttpRequest
from django.conf import settings

from logement.libs.notifyer.mail import send_mail, send_auto_email

MAIL_TEMPLATE="""
%(nb)s nouveaux logements disponibles !
https://%(domain)s/'
"""
def get_mail(nb):
    return MAIL_TEMPLATE % {
        "nb": nb,
        "domain": settings.DOMAIN
    }



def mail_notify(nb):
    for mail in settings.EMAILS:
        return send_auto_email(mail, f"{nb} nouveaux logemnts disponibles", get_mail(nb))

def notify(req : HttpRequest, annocnes):
    mail_notify(len(annocnes))

