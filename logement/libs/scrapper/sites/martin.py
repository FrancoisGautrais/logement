import json
import re

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, PageScrapper, \
    HelperJson

url = "https://www.cabinet-martin.fr/location/appartement/rennes/3-pieces--4-pieces/600-euros-minimum/950-euros-maximum"



class MartinAnnonceScrapper(PageScrapper):
    DOMAIN="www.cabinet-martin.fr"
    QUERY_TITLE = HelperHtmlText("h1")
    QUERY_CONTENT = HelperHtmlText(".rendered-body > p")
    QUERY_ADDRESS = HelperHtmlText("small")
    QUERY_ID = HelperHtmlAttr("article", "id")
    QUERY_IMGS = HelperHtmlAttr(".gallery>img", "src", cast=lambda x : [x])
    QUERY_PRIX = HelperHtmlText("small")
    QUERY_PHONES = HelperHtmlText(".conseiller", cast=PageScrapper.find_phone)
    REG = re.compile(r"(?P<surface>\d+) ?m²")

    def get_imgs(self):
        return [x.attrib.get("href") for x in self.d(".photos.hidden > a")]

    def get_surface(self):
        ret = re.findall(self.REG, self.d("h1").text())
        return ret[0] if ret else None

class MartinThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.cabinet-martin.fr"
    QUERY_TITLE =  HelperHtmlText("h2 > a")
    QUERY_ID = HelperHtmlAttr("article", "id")
    QUERY_PRIX = HelperHtmlText(".prix")
    QUERY_URL = HelperHtmlAttr("h2 > a", "href", cast=lambda x: f"https://www.cabinet-martin.fr{x}")

class MartinScrapper(ListScrapper):
    DOMAIN="www.cabinet-martin.fr"

    def find_elements(self):
        return [ x for x in self.d(".list-item")]


if __name__ == "__main__":
    from logement.libs.scrapper import scrap
    x = scrap(url)
    for v in x.elements:
        d = v.visit()
        print(f"ID = {d.custom_id}")
        print(f"title = {d.title}")
        print(f"content = {d.content}")
        print(f"imgs = {d.imgs}")
        print(f"prix = {d.prix}")
        print(f"phone = {d.phones}")
        print(f"surface = {d.surface}")
        print(f"address = {d.address}")
        print("\n\n")

