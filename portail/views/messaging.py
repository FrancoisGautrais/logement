from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message

from logement.libs.notifyer import push
from logement.libs.utils import need_auth


@need_auth
def token(req : HttpRequest, token : str):
    x = len(FCMDevice.objects.filter(registration_id=token))
    if not x:
        FCMDevice.objects.create(
            device_id=token,
            registration_id=token,
            type = "android",
        )
    return HttpResponse()

@need_auth
def send(req : HttpRequest):
    push.send_notif_to_all("Tets", "Ça marche")
    return HttpResponse()


@need_auth
def subscribe_page(req : HttpRequest):
    return render(req, "subscribe.html",  {})



urls = [
    path("subscribe", subscribe_page),
    path("subscribe/<str:token>", token),
    path("send", send),
]