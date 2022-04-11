import json
import re

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, AutoText, AutoAttr, PageScrapper, \
    AutoData

DOMAIN=""
url = "https://www.cabinet-XXXX.fr/location/appartement/rennes/3-pieces--4-pieces/600-euros-minimum/950-euros-maximum"



class XXXXAnnonceScrapper(PageScrapper):
    DOMAIN=DOMAIN
    QUERY_TITLE = AutoText("h1")
    QUERY_CONTENT = AutoText(".rendered-body > p")
    QUERY_ADDRESS = AutoText("small")
    QUERY_ID = AutoAttr("article", "id")
    QUERY_IMGS = AutoAttr(".gallery>img", "src", cast=lambda x : [x])
    QUERY_PRIX = AutoText("small")
    QUERY_PHONES = AutoText(".conseiller", cast=PageScrapper.find_phone)
    REG = re.compile(r"(?P<surface>\d+) ?m²")

    def get_imgs(self):
        return [x.attrib.get("src") for x in self.d(".photos.hidden > a")]

    def get_surface(self):
        ret = re.findall(self.REG, self.d("h1").text())
        return ret[0] if ret else None

class XXXXThubnailScrapper(ThumbnailScrapper):
    DOMAIN=DOMAIN
    QUERY_TITLE =  AutoText("h2 > a")
    QUERY_ID = AutoAttr("article", "id")
    QUERY_PRIX = AutoText(".prix")
    QUERY_URL = AutoAttr("h2 > a", "href", cast=lambda x: f"{DOMAIN}{x}")

class XXXXScrapper(ListScrapper):
    DOMAIN=DOMAIN

    def find_elements(self):
        return [ x for x in self.d(".list-item")]


XXXXThubnailScrapper.register()
XXXXAnnonceScrapper.register()
XXXXScrapper.register()

if __name__ == "__main__":
    x = ListScrapper.scrap(url)
    for v in x.data:
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

