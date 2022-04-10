from django.http import HttpRequest
from django.conf import settings

from logement.libs.notifyer import push
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
    nb = len(annocnes)
    mail_notify(nb)
    push.send_notif_to_all(f"Nouveaux logments", f"{nb} nouvelles annonces disponible !")


