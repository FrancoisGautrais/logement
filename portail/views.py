import json

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


def page(req : HttpRequest):
    data = {
        "liste" : list(Annonce.objects.all().order_by("-creation_date"))
    }
    return render(req, "element.html",  data)