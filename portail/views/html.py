import time
from pathlib import Path

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path

from django.views.decorators.cache import never_cache

from logement.libs import score
from logement.libs.utils import need_auth
from portail.models import Annonce, Filter
from portail.views import annonce


@never_cache
@need_auth
def page_list(req : HttpRequest):

    param = req.GET or {}
    rel = param.get("is_relevant")
    if rel is not None: rel = rel.lower() in ("true", "1")
    disable = param.get("disable", False)
    if isinstance(disable, str) and disable.lower() == "none":
        disable = None
    elif isinstance(disable, str) and (disable.lower()=="true" or disable.lower()=="1"):
        disable=True
    else:
        disable=False
    kwargs = {
        "is_relevant": True,
        "score__gte" : param.get("score", 0),
    }
    if disable is not None:
        kwargs["disable"] = disable

    data = {
        "liste" : list(Annonce.objects.filter(**kwargs).order_by("-creation_date"))
    }
    return render(req, "element.html",  data)

@never_cache
@need_auth
def page_list_all(req : HttpRequest):
    data = {
        "liste" : list(Annonce.objects.all().order_by("-creation_date"))
    }
    return render(req, "element.html",  data)

@never_cache
@need_auth
def filtres(req : HttpRequest):
    if req.method == "POST":
        data = req.POST
        include = data.get("include").replace("\r","")
        exclude = data.get("exclude").replace("\r","")
        score.set_filtres(include, exclude)
        if data.get("validate_and_reload") is not None:
            annonce.update_score(req)
    elif req.method=="GET":
        include = "\n".join(Filter.include())
        exclude = "\n".join(Filter.exclude())
    data = {
        "include": include,
        "exclude" : exclude
    }
    return render(req, "filtres.html", data)


urls = [
    path("", page_list),
    path("all", page_list_all),
    path("tous", page_list_all),
    path("filtres", filtres),
]