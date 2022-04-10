from fcm_django.models import FCMDevice
from firebase_admin.messaging import Notification, Message


def send_notif_to_all(title, body, image=None):
    msg = Message(
        notification=Notification(title=title, body=body, image=image or "/images/image.jpg")
    )
    for device in FCMDevice.objects.all():
        device.send_message(msg)

