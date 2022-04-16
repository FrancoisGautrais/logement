import datetime
import json
from pathlib import Path

import pytz
from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.views.decorators.cache import never_cache

from logement.libs.scrapper.urls import LOOKUP_URLS
from logement.libs.utils import find_domain, need_auth
from portail.models import Error, Options, Annonce


@never_cache
@need_auth
def errors(req: HttpRequest):
    post = (req.POST if hasattr(req, "POST") else None) or {}
    errors = {k: v for k, v in req.GET.items()}
    errors.update(post)
    kwargs={}
    for key in ["domain", "url", "exception_type", "classe"]:
        if key in errors: kwargs[key]=errors[key]

    sort = errors.get("order_by", "-last_date")
    count = errors.get("count")
    liste = Error.objects.filter().order_by(sort)
    total = len(liste)
    if count:
        liste=liste[:min(int(count), len(liste))]

    data = {
        "count" : total,
        "shown" : len(liste),
        "liste" : liste,
        "request" : req
    }
    return render(req, "errors.html", data)

TITLE_NAME = {
    "ok": "OK",
    "warning" : "Attention",
    "error" : "Erreur",
}


@never_cache
@need_auth
def status(req : HttpRequest):
    WARNING_THRESOLD_SECONDS = 3600
    CLEAR_WARGING_THRESOLD_SECONDS = 3600*24*3
    domains = []

    now = datetime.datetime.now(tz=pytz.timezone("Europe/Paris"))
    d_last1 = now - datetime.timedelta(seconds=3600)
    d_last24 = now - datetime.timedelta(days=1)
    d_last72 = now - datetime.timedelta(days=3)
    for url in LOOKUP_URLS+[None]:
        domaine = find_domain(url)

        all = Error.from_domain(domaine)
        count = len(all)
        last1 = len(all.filter(last_date__gte=d_last1))
        last24 = len(all.filter(last_date__gte=d_last24))
        last72 = len(all.filter(last_date__gte=d_last72))
        err = all[0] if len(all) else None
        status = "ok"
        if err:
            delta = datetime.datetime.now(tz=pytz.timezone("Europe/Paris")) - err.last_date
            if delta.seconds<WARNING_THRESOLD_SECONDS:
                status = "error"
            elif delta.seconds<CLEAR_WARGING_THRESOLD_SECONDS:
                status="warning"

        domains.append({
            "domain" : domaine,
            "status" : status,
            "exception" : err,
            "date" : err.last_date if err else "",
            "count" : count,
            "count1" : last1,
            "count24" : last24,
            "count72" : last72,
        })
    status = "ok"
    if any(x.get("status")=="error" for x in domains):
        status = "error"
    elif any(x.get("status")=="warning" for x in domains):
        status="warning"



    for obj in domains:
        obj["title"]=TITLE_NAME.get(obj.get("status"), "inconnu")

    general = domains.pop()

    duration = Options.get_value("last_poll_duration")
    duration = ("%.3fs" % duration) if duration else "- s"
    annonces_by_domains=[]
    for url in LOOKUP_URLS:
        domaine = find_domain(url)
        all = Annonce.objects.filter(domain=domaine).order_by("-creation_date")
        count = len(all)
        last1 = len(all.filter(creation_date__gte=d_last1))
        last24 = len(all.filter(creation_date__gte=d_last24))
        last72 = len(all.filter(creation_date__gte=d_last72))
        last = all[0] if all else None
        annonces_by_domains.append({
            "domain" : domaine,
            "annonce" : last,
            "date" : last.creation_date if last else "",
            "count" : count,
            "count1" : last1,
            "count24" : last24,
            "count72" : last72,
            "url" : url
        })

    dates = [x.get("date") for x in domains+[general] if x.get("date")]
    data = {
        "annonces" : {
            "annonces" : annonces_by_domains,
            "count": sum(x.get("count") for x in annonces_by_domains),
            "count1": sum(x.get("count1") for x in annonces_by_domains),
            "count24": sum(x.get("count24") for x in annonces_by_domains),
            "count72": sum(x.get("count72") for x in annonces_by_domains),
            "date": min(x.get("date") for x in annonces_by_domains),
        },
        "errors" : {
            "domains" : domains,
            "general" : general,
            "status" : status,
            "title" : TITLE_NAME[status],
            "count" : sum(x.get("count") for x in domains+[general]),
            "count1" : sum(x.get("count1") for x in domains+[general]),
            "count24" : sum(x.get("count24") for x in domains+[general]),
            "count72" : sum(x.get("count72") for x in domains+[general]),
            "date" : min(dates) if dates else "",
        },
        "request" : req,
        "last_poll" : Options.get_value("last_poll", "aucun"),
        "last_poll_duration" : duration,
    }

    return render(req, "status.html", data)


@need_auth
def remove(req : HttpRequest, id : int):
    errors = {k: v for k, v in req.GET.items()}
    try:
        data = Error.objects.get(id=id)
    except Error.DoesNotExist:
        if errors.get("redirect"):
            return HttpResponseRedirect(errors.get("redirect"))
        return HttpResponse(json.dumps({
            'status': "ok",
            "data": {
                "suppressed": 0
            }
        }), content_type="applciation/json")

    data.delete()

    if errors.get("redirect"):
        return HttpResponseRedirect(errors.get("redirect"))
    return HttpResponse(json.dumps({
        'status' : "ok",
        "data" : {
            "suppressed" : 1
        }
    }), content_type="applciation/json")


@need_auth
def remove_all(req : HttpRequest, id : int):
    post = (req.POST if hasattr(req, "POST") else None) or {}
    errors = {k: v for k, v in req.GET.items()}
    errors.update(post)
    kwargs = {}
    for key in ["domain", "url", "exception_type", "classe"]:
        if key in errors: kwargs[key] = errors[key]

    sort = errors.get("order_by", "-last_date")
    count = errors.get("count")
    liste = Error.objects.filter().order_by(sort)
    total = len(liste)
    if count:
        liste = liste[:min(int(count), len(liste))]

    nb = len(liste)
    for elem in liste:
        elem.delete()

    if errors.get("redirect"):
        return HttpResponseRedirect(errors.get("redirect"))
    return HttpResponse(json.dumps({
        'status' : "ok",
        "data" : {
            "suppressed" : nb
        }
    }), content_type="applciation/json")

urls = [
    path("status", status),
    path("errors", errors),
    path("errors/remove/<int:id>", remove),
    path("errors/remove/all", remove_all),
]