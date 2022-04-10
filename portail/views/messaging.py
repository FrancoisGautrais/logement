from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import path
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message


def fb_messaging(req : HttpRequest):
    x = settings.BASE_DIR / "www" / "_firebase-messaging-sw.js"
    return HttpResponse(content=x.read_bytes(), content_type="text/javascript")

def token(req : HttpRequest):
    return HttpResponse()

def send(req : HttpRequest):
    device = FCMDevice.objects.create(
        device_id='fasUbzsOBwBeK8f142WNiu:APA91bFMJgB5QPNwlOygU97Sz90tbfMFobCGy-aiaebc7EY1CA_JJp3JLooRkiDrVrZ9PAP-zJyCIXl5hb28cpttNrRZv1UheHPMzairNj_BxOM54nM457tg2OK-jBjUgJlcQZnOUbfU',
        registration_id='fasUbzsOBwBeK8f142WNiu:APA91bFMJgB5QPNwlOygU97Sz90tbfMFobCGy-aiaebc7EY1CA_JJp3JLooRkiDrVrZ9PAP-zJyCIXl5hb28cpttNrRZv1UheHPMzairNj_BxOM54nM457tg2OK-jBjUgJlcQZnOUbfU',
        type = "android",
    )
    msg = Message(
        notification=Notification(title="title", body="text", image="url")
    )
    device.send_message(msg)
    return HttpResponse()

urls = [
    path("firebase-messaging-sw.js", fb_messaging),
    path("token", token),
    path("send", send),
]