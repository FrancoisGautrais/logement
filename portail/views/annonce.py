import datetime
import json
import sys
import urllib.parse

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

from logement.libs import scrapper, score
from logement.libs.notifyer.notify import notify
from logement.libs.scrapper.base.location_scrapper import ScrapRuntimeException
from logement.libs.scrapper.urls import LOOKUP_URLS

from portail.models import Annonce, Options


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

def write_exception(exc : ScrapRuntimeException):
    with open(settings.ERROR_FILE, "a") as file:
        data = "\n".join([
            f"===================== Exception le {datetime.datetime.now()} ============================",
            f"Classe : {exc.scrapper}",
            f"Content : {exc.content}",
            f"=================================================\n\n",
        ])
        print(data, file=sys.stderr)
        file.write(data)
        file.flush()


def strify(x):
    return {
        str(k): v if isinstance(v, (int, bool, float, str)) or v is None else str(v) for k, v in x.items()
    }



# Create your views here.
def poll(req : HttpRequest):
    news=[]
    filtereds = []
    ret = {}
    for url in LOOKUP_URLS:
        _url = str(url)
        domain = {
            "url" : _url,
            "elements" : [],
            "error" : False,
        }
        ret[_url.split("?")[0]]=domain

        try:
            scrapped = scrapper.scrap(url)
        except ScrapRuntimeException as exc:
            write_exception(exc)
            domain["error"]=True
            continue

        for thubnail in scrapped.elements:
            current = thubnail.__class__

            page = {
                "thubnail" : None,
                "error" : False,
                "visited": False,
                "page" : None,
                "added" : False
            }
            domain["elements"].append(page)
            try:
                js = thubnail.as_dict()
                page["thubnail"]=strify(js)

                if not Annonce.exists(js):
                    complete = thubnail.visit()
                    page["visited"]=True

                    current = complete.__class__
                    complete_js = complete.as_dict()
                    complete_js["url"]=js.get("url")

                    page["page"]=strify(complete_js)

                    if not Annonce.exists(complete_js):
                        obj = Annonce.create(complete_js)
                        if obj.is_relevant and obj.score>=settings.CRITERES.get("score.min", 0):
                            filtereds.append(obj)
                        news.append(obj)

                        page["added"] = True

            except ScrapRuntimeException as exc:
                page["error"] = True
                write_exception(exc)
                continue
            except Exception as exc:
                page["error"] = True
                ex = ScrapRuntimeException(exc, current)
                write_exception(ex)
                continue

    if filtereds:
        notify(req, filtereds)
    Options.set("last_poll", str(datetime.datetime.now()))

    data = {
        "nb_added" : len(news),
        "nb_relevant_added" : len(filtereds)
    }
    if req.GET.get("verbose", "").lower() not in ("", "0", "false"):
        data["domains"] = ret



    return HttpResponse(json.dumps(data, indent=2), content_type="application/json" )

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