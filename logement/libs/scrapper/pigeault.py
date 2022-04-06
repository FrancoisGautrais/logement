import json

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.location_scrapper import ListScrapper, ThumbnailScrapper, AutoText, AutoAttr, PageScrapper, \
    AutoData

url = "https://www.pigeaultimmobilier.com/location/?sous-categorie%5B%5D=1455&agences%5B%5D=26548&prix_min=500&prix_max=950&submitted=1&o=date-desc&action=load_search_results&wia_6_type=location&searchOnMap=0&wia_1_reference="



class PigeaultAnnonceScrapper(PageScrapper):
    DOMAIN="www.pigeaultimmobilier.com"
    QUERY_ID = AutoAttr(".estate", "data-id")
    QUERY_TITLE = AutoText("#contenu > h2 > span")
    QUERY_PRIX = AutoText(".prix")
    QUERY_CONTENT = AutoText("#contenu > p")
    QUERY_ADDRESS = AutoText("small.h6")
    QUERY_SURFACE = AutoText(".surface")
    QUERY_PHONES = AutoAttr("#phone-top", "data-number", cast=lambda x: [x])

    def get_id(self):
        for x in self.d("article"):
            return x.attrib.get("id")

    def get_imgs(self):
        ret = []
        for x in self.d("figure > a > img"):
            img = x.attrib.get('src')
            if img:
                ret.append(f"https://www.Pigeault-immobilier.fr/{img}")

        return ret

class PigeaultThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.pigeaultimmobilier.com"
    QUERY_TITLE =  AutoAttr("img", "alt")
    QUERY_ID = AutoAttr("article", "id")
    QUERY_PRIX = AutoText(".prix")
    QUERY_URL = AutoAttr("article>div>a", "href")



class PigeaultScrapper(ListScrapper):
    DOMAIN="www.pigeaultimmobilier.com"

    def find_elements(self):
        return [ x for x in self.d("article")]


PigeaultThubnailScrapper.register()
PigeaultAnnonceScrapper.register()
PigeaultScrapper.register()

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

