import json
import re

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.connector import JsonConnector
from logement.libs.scrapper.base.helpers import HelperHtml, HelperJson, HelperConst
from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, PageScrapper, \
    HelperJson
from logement.libs.scrapper.base.request import Post

DOMAIN="fnc-api.prod.fonciatech.net"
url = "https://fr.foncia.com/location/par-carte/appartement?geoBox=48.09568415298487;-1.6571526791896154_48.124558715078734;-1.7309089969658011&prix=450--950&surface=50--100&zoom=14&advanced=#results"



class FonciaAnnonceScrapper(PageScrapper):
    DOMAIN=DOMAIN
    CONNECTOR = JsonConnector
    QUERY_TITLE =  HelperJson("libelle")
    QUERY_ID = HelperJson("reference")
    QUERY_PRIX = HelperJson("loyer")
    QUERY_CONTENT = HelperJson("description")
    QUERY_ADDRESS = HelperJson("localisation", "adresse")+HelperJson("localisation", "ville")
    QUERY_IMGS = HelperJson("medias")
    QUERY_PHONES = HelperConst(["02 99 79 41 14"])
    QUERY_SURFACE = HelperJson("surface", "carrez")

    def init(self):
        return self.d

class FonciaThubnailScrapper(ThumbnailScrapper):
    DOMAIN=DOMAIN
    CONNECTOR = JsonConnector
    QUERY_TITLE =  HelperJson("libelle")
    QUERY_ID = HelperJson("reference")
    QUERY_PRIX = HelperJson("loyer")
    QUERY_URL = HelperConst("https://fnc-api.prod.fonciatech.net/annonces/annonces/location/")+HelperJson("reference", cast=str)

    def init(self):
        return self.d

class FonciaScrapper(ListScrapper):
    DOMAIN=DOMAIN
    CONNECTOR = JsonConnector
    QUERY_ELEMENTS = HelperJson("annonces", target="response_json")



if __name__ == "__main__":
    post = Post("https://fnc-api.prod.fonciatech.net/annonces/annonces/search",
                '{"type":"location","filters":{"typesBien":["appartement"],"surface":{"min":50,"max":100},"prix":{"min":450,"max":950},"map":{"geoBox":{"bottomRight":{"lon":-1.6571526791896154,"lat":48.09568415298487},"topLeft":{"lon":-1.7309089969658011,"lat":48.124558715078734}},"zoom":14}},"expandNearby":true,"size":15}',
                headers={"Content-Type": "application/json"})

    from logement.libs.scrapper import scrap
    x = scrap(post)
    for v in x.elements:
        d = v.visit()
        print(f"ID = {d.custom_id}")
        print(f"url = {d.url}")
        print(f"title = {d.title}")
        print(f"content = {d.content}")
        print(f"imgs = {d.imgs}")
        print(f"prix = {d.prix}")
        print(f"phone = {d.phones}")
        print(f"surface = {d.surface}")
        print(f"address = {d.address}")
        print("\n\n")

