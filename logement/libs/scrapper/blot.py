import json

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.location_scrapper import ListScrapper, ThumbnailScrapper, AutoText, AutoAttr, PageScrapper, \
    AutoData

url = "https://www.blot-immobilier.fr/habitat/location/appartement--appartement-neuf/ille-et-vilaine/rennes/?t3=true&t4=true"


class BlotAnnonceScrapper(PageScrapper):
    DOMAIN="www.blot-immobilier.fr"
    QUERY_TITLE = AutoText("h1")
    QUERY_CONTENT = AutoData("mainEntity", "description")
    QUERY_ADDRESS = AutoText(".adresse")
    QUERY_ID = AutoText("small")
    QUERY_IMGS = AutoAttr(".gallery>img", "src", cast=lambda x : [x])
    QUERY_PRIX = AutoText(".prix>strong")


    def get_imgs(self):
        ret = []
        for x in self.d(".gallery>img"):
            img = x.attrib.get('src')
            if img:
                ret.append(f"https://www.blot-immobilier.fr/{img}")

        return ret

class BlotThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.blot-immobilier.fr"
    QUERY_TITLE =  AutoText(".ref")
    QUERY_ID = AutoText(".ref")
    QUERY_PRIX = AutoText(".prix>strong")
    QUERY_ADDRESS = AutoText(".annAdresse")
    QUERY_CONTENT = AutoText("#descriptif")
    QUERY_URL = AutoAttr("a", "href", cast=lambda x: f"https://www.blot-immobilier.fr{x}")



class BlotScrapper(ListScrapper):
    DOMAIN="www.blot-immobilier.fr"

    def find_elements(self):
        return [ x for x in self.d(".search_results > .container > .bloc_annonce")]


BlotThubnailScrapper.register()
BlotAnnonceScrapper.register()
BlotScrapper.register()

if __name__ == "__main__":
    x = ListScrapper.scrap(url)
    for v in x.data:
        d = v.visit()
        print(f"ID = {d.id}")
        print(f"title = {d.title}")
        print(f"content = {d.content}")
        print(f"imgs = {d.imgs}")
        print(f"prix = {d.prix}")
        print(f"phone = {d.phones}")
        print(f"surface = {d.surface}")
        print(f"address = {d.address}")
        print("\n\n")

