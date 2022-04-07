import json
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from portail.models import Annonce
from logement.libs import scrapper, score
from django.conf import settings

# Create your views here.
def poll(req : HttpRequest):
    news=[]
    for url in settings.LOOKUP_URLS:
        scrapped = scrapper.scrap(url)
        for thubnail in scrapped.data:
            js = thubnail.as_dict()
            if not Annonce.exists(js):
                complete = thubnail.visit()
                complete_js = complete.as_dict()
                complete_js["url"]=js.get("url")
                if not Annonce.exists(complete_js):
                    obj = Annonce.create(complete_js)
                    news.append(obj)

    return HttpResponse(len(news))


def page_list(req : HttpRequest):

    param = req.GET or {}
    rel = param.get("is_relevant")
    if rel is not None: rel = rel.lower() in ("true", "1")
    kwargs = {
        "is_relevant": True,
        "score__gte" : param.get("score", 0)
    }

    data = {
        "liste" : list(Annonce.objects.filter(**kwargs).order_by("-creation_date"))
    }
    return render(req, "element.html",  data)

def download(req : HttpRequest, id : str):
    cache = settings.CACHE_PATH / f"{id}.zip"
    if cache.is_file():
        ret = HttpResponse(content=cache.read_bytes(), content_type="application/zip", )
    else:
        return HttpResponse()


def generate_note(tree, data):
    out = []
    if data.get("note"):
        out.append(f"Note:\n{data.get('note')}")

    out.append(f"Liste des fichiers:\n{tree}")
    return "\n\n".join(out)



def integrate_zip(dir, data):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        zipfile = tmp / "data.zip"
        shutil.copy(settings.DATA_PATH / "data.zip", zipfile)
        with ZipFile(zipfile, "w") as zip:
            for file in dir.iterdir():
                if not file.is_file(): continue
                zip.writestr(file.name, file.read_bytes())
    return output.read_bytes()

def update_score(request : HttpRequest):
    score.reload()
    for x in Annonce.objects.all():
        old_score = x.score
        old_rev = x.is_relevant
        x.score = score.score(x)
        x.is_relevant = score.is_relevant(x)
        if x.is_relevant != old_rev or x.score != old_score:
            x.save()
    return page_list(request)



def upload(request : HttpRequest):
    if request.method == 'POST':
        with tempfile.TemporaryDirectory() as dir :
            dir = Path(dir)
            files = request.FILES.getlist("files")
            for f in files:
                with open(dir / f.name, "wb") as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
            integrate_zip(dir, request.POST)
            return HttpResponse()

def page(req : HttpRequest):
    x = settings.BASE_DIR / "www" / "index.html"
    return HttpResponse(content=x.read_bytes(), content_type="text/html")


def libs(req : HttpRequest):
    x = settings.BASE_DIR / "www" / "lib.js"
    return HttpResponse(content=x.read_bytes(), content_type="application/javascript")

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



