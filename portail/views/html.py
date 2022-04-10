from django.http import HttpRequest
from django.shortcuts import render
from django.urls import path

from portail.models import Annonce


def page_list(req : HttpRequest):

    param = req.GET or {}
    rel = param.get("is_relevant")
    if rel is not None: rel = rel.lower() in ("true", "1")
    kwargs = {
        "is_relevant": True,
        "score__gte" : param.get("score", 0),
        "disable" : False
    }

    data = {
        "liste" : list(Annonce.objects.filter(**kwargs).order_by("-creation_date"))
    }
    return render(req, "element.html",  data)

def page_list_all(req : HttpRequest):

    param = req.GET or {}
    data = {
        "liste" : list(Annonce.objects.all().order_by("-creation_date"))
    }
    return render(req, "element.html",  data)


urls = [
    path("", page_list),
    path("all", page_list_all),
    path("tous", page_list_all),
]