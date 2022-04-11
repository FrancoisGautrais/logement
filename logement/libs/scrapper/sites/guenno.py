import json
import re

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, AutoText, AutoAttr, PageScrapper, \
    AutoData

DOMAIN="www.guenno.com"
url = "https://www.guenno.com/biens/recherche?realty_type[]=1&mandate_type=2&number_room[]=3&min_surface=&town=RENNES&price_max=950"



class GuennoAnnonceScrapper(PageScrapper):
    DOMAIN=DOMAIN
    QUERY_ID = AutoData("id", cast=str)
    QUERY_TITLE = AutoText("#realty_area")
    QUERY_CONTENT = AutoData("description")
    QUERY_ADDRESS = AutoText("#realty_area")
    QUERY_IMGS = AutoData("pictures")
    QUERY_SURFACE = AutoData("surface")
    REG = re.compile(r"(?P<surface>\d+) ?m²")


    def get_prix(self):
        return self.data.get("price")+self.data.get("provisions_feed")

    def get_imgs(self):
        return [x.attrib.get("src") for x in self.d(".print-picture")]


    def init(self):
        for line in  str(self.d).split("\n"):
            if line.startswith("    var realty  = "):
                return json.loads(line[18:])


class GuennoThubnailScrapper(ThumbnailScrapper):
    DOMAIN=DOMAIN
    QUERY_ID = AutoAttr("article", "id")
    QUERY_PRIX = AutoText(".realty_price")
    QUERY_URL = AutoAttr(".link-block", "href", cast=lambda x: f"{x}")

class GuennoScrapper(ListScrapper):
    DOMAIN=DOMAIN

    def find_elements(self):
        return [ x for x in self.d("article")]


GuennoThubnailScrapper.register()
GuennoAnnonceScrapper.register()
GuennoScrapper.register()

if __name__ == "__main__":
    x = ListScrapper.scrap(url)
    for d in x.data:
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

