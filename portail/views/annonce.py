from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from logement.libs import scrapper, score
from logement.libs.notifyer.notify import notify

from portail.models import Annonce


def disable(req : HttpRequest, id : int):
    elem = Annonce.objects.get(id=id)
    elem.disable=True
    elem.save()
    return HttpResponseRedirect("/")


def enable(req : HttpRequest, id : int):
    elem = Annonce.objects.get(id=id)
    elem.disable=False
    elem.save()
    return HttpResponseRedirect("/")



def show_annonce(req : HttpRequest, id : int):
    elem = Annonce.objects.get(id=id)
    data = {
        "elem" : elem
    }
    return render(req, "page.html",  data)



# Create your views here.
def poll(req : HttpRequest):
    news=[]
    filtereds = []
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
                    if obj.is_relevant and obj.score>=settings.CRITERES.get("score.min", 0):
                        filtereds.append(obj)
                    news.append(obj)
    if filtereds:
        notify(req, filtereds)
    return HttpResponse(len(news))



def update_score(request : HttpRequest):
    score.reload()
    for x in Annonce.objects.all():
        old_score = x.score
        old_rev = x.is_relevant
        x.score = score.score(x)
        x.is_relevant = score.is_relevant(x)
        if x.is_relevant != old_rev or x.score != old_score:
            x.save()
    return HttpResponseRedirect("/")

urls = [
    path("poll", poll),
    path("update", update_score),
    path("annonce/disable/<int:id>", disable),
    path("annonce/enable/<int:id>", enable),
    path("annonce/<int:id>", show_annonce),
]