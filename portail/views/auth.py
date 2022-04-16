from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path

def _login(req : HttpRequest):
    redirect = settings.LOGIN_REDIRECT_URL
    if req.POST and req.POST.get("redirect"):
        redirect = req.POST.get("redirect")
    if req.GET and req.GET.get("redirect"):
        redirect = req.GET.get("redirect")
    if req.user and req.user.is_authenticated:
        return HttpResponseRedirect(redirect)


    if req.method == "GET":
        data = {
            "redirect": redirect
        }
        return render(req, "login.html", data)
    elif req.method == "POST":
        user = authenticate(req,
                            username=req.POST.get("username"),
                            password=req.POST.get("password"))
        if user is not None:
            login(req, user)
            return HttpResponseRedirect(redirect)
        else:
            data = {
                "redirect": redirect,
                "message" : "Mauvais login ou mot de passe"
            }
            return render(req, "login.html", data)


    return HttpResponseRedirect(settings.LOGIN_URL)


def _logout(req : HttpRequest):
    logout(req)
    return HttpResponseRedirect(settings.LOGIN_URL)

urls = [
    path("logout", _logout),
    path("login", _login),
]
