

import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import path

from logement.libs.notifyer.notify import notify
from portail.models import Annonce


def mail(req : HttpRequest):
    notify(req, list(Annonce.objects.all())[:-5])
    return HttpResponse("ok")



def push(req : HttpRequest):
    notify(req, list(Annonce.objects.all())[:-5])
    return HttpResponse("ok")


urls = [
    path("mail", mail),
    path("push", push),
]