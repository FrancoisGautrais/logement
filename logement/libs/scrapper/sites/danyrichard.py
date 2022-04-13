import json
import re

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.helpers import HelperConst
from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, \
    PageScrapper, HelperJson

DOMAIN="www.dany-richard-immo.com"
url = "http://www.dany-richard-immo.com/location/"



class DanyRichardAnnonceScrapper(PageScrapper):
    DOMAIN=DOMAIN
    QUERY_TITLE = HelperHtmlText("h1")
    QUERY_CONTENT = HelperHtmlText(".col-3-small-1")
    QUERY_ADDRESS = HelperJson("address")
    QUERY_ID = HelperJson("référence")
    QUERY_PRIX = HelperJson("prix")
    QUERY_SURFACE = HelperJson("surface")
    QUERY_PHONES = HelperConst(["02 99 31 01 00"])

    def get_imgs(self):
        return [x.attrib.get("data-image-large") for x in self.d(".js-product--image__thumb")]

    def init(self):
        data={}
        for line in self.d(".product--attributes>ul>li"):
            key, value = line.text.split(":", 1)
            data[key.lower().strip()]=value
        data["address"]=data.get("ville", "")+" "+data.get("quartier", "")
        return data


def do_id(x):
    x = x.split("\n")[0]
    x.split(':')[-1].strip()
    return x

class DanyRichardThubnailScrapper(ThumbnailScrapper):
    DOMAIN=DOMAIN
    QUERY_TITLE =  HelperHtmlText(".txtright")
    QUERY_ID = HelperHtmlText(".txtright", cast=lambda x: do_id)
    QUERY_PRIX = HelperHtmlText(".products-list--item__price")
    QUERY_URL = HelperHtmlAttr("figure>a", "href", cast=lambda x: f"http://{DOMAIN}{x}")


    def get_id(self):
        x = self.d(".txtright")
        return do_id(x.text())

class DanyRichardScrapper(ListScrapper):
    DOMAIN=DOMAIN

    def find_elements(self):
        return [ x for x in self.d("article")]


if __name__ == "__main__":
    from logement.libs.scrapper import scrap
    x = scrap(url)
    for d in x.elements:
        d = d.visit()
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

