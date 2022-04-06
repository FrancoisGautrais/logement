import json
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from portail.models import Annonce
from logement.libs.scrapper import ListScrapper
from django.conf import settings

# Create your views here.
def poll(req : HttpRequest):
    news=[]
    for url in settings.LOOKUP_URLS:
        scrapped = ListScrapper.scrap(url)
        for thubnail in scrapped.data:
            js = thubnail.as_dict()
            if not Annonce.exists(js):
                complete = thubnail.visit()
                complete_js = complete.as_dict()
                complete_js["url"]=js.get("url")
                if not Annonce.exists(complete_js):
                    obj = Annonce.create(complete_js)
                    news.append(obj)
                    print(complete_js)

    return HttpResponse(len(news))


def page_list(req : HttpRequest):
    data = {
        "liste" : list(Annonce.objects.all().order_by("-creation_date"))
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

def mktree(zip):
    with tempfile.TemporaryDirectory() as temp:


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

