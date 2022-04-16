

import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.urls import path

from logement.libs.notifyer.notify import notify
from logement.libs.utils import need_auth
from portail.models import Annonce


@need_auth
def mail(req : HttpRequest):
    notify(req, list(Annonce.objects.all())[:-5])
    return HttpResponse("ok")



@need_auth
def push(req : HttpRequest):
    notify(req, list(Annonce.objects.all())[:-5])
    return HttpResponse("ok")


urls = [
    path("mail", mail),
    path("push", push),
]