import json

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, AutoText, AutoAttr, PageScrapper, \
    AutoData

url = "https://www.ouestfrance-immo.com/louer/appartement--3-pieces_4-pieces/?lieux=100003,100013&prix=0_950"


class OuestFranceThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.ouestfrance-immo.com"
    QUERY_PRIX = AutoText(".annPrix")
    QUERY_TITLE = AutoText(".annTitre")
    QUERY_ADDRESS = AutoText(".annAdresse")
    QUERY_CONTENT = AutoText(".annTexte")
    QUERY_URL = AutoAttr(".annLink", "href", cast=lambda x: f"https://www.ouestfrance-immo.com{x}")
    QUERY_IMGS = AutoAttr(".annPhoto", "data-original", cast=lambda x: [x], )


    def get_surface(self):
        q = self.d(".annCriteres")
        for x in q:
            for div in x:
                for unit in div.xpath("span"):
                    if "m²" in unit.text:
                        return div.text
        return None


    def get_id(self):
        for div in self.d("div"):
            if div.attrib.get("data-id") != None:
                return  div.attrib.get("data-id")

    def get_phones(self):
        x = self.glob(f"#contact_tel_div_{self.custom_id}_1")
        phones = []
        for div in x:
            for ret in pq(div)(".num"):
                tmp = self.find_phone(ret.text)
                if tmp:
                    phones.extend(tmp)
        return phones


class OuestFranceAnnonceScrapper(PageScrapper):
    DOMAIN="www.ouestfrance-immo.com"
    QUERY_ID = AutoAttr("#idAnnonce", "value")
    QUERY_PRIX = AutoAttr("#prix_reel", "value")
    QUERY_TITLE = AutoData("mainEntity", "name")
    QUERY_CONTENT = AutoData("mainEntity", "description")
    QUERY_IMGS = AutoData("mainEntity", "photo", "contentUrl")
    QUERY_ADDRESS = AutoText(".adresse")

    def init(self):
        for x in self.d("script"):
            if x.attrib.get("type") == "application/ld+json":
                return json.loads(x.text)


    def get_surface(self):
        q = self.d(".ann-criteres")
        for x in q:
            for div in x:
                for unit in div.xpath("span"):
                    if "m²" in unit.text:
                        return div.text
        return None


    def get_phones(self):
        x = self.glob(f"#contact_tel_div_{self.custom_id}_1")
        phones = []
        for div in x:
            for ret in pq(div)(".num"):
                tmp = self.find_phone(ret.text)
                if tmp:
                    phones.extend(tmp)
        return phones


class OuestFranceScrapper(ListScrapper):
    DOMAIN="www.ouestfrance-immo.com"

    def find_elements(self):
        return [ x for x in self.d(".annLink") if x.attrib.get("data-trk-payload")]


OuestFranceThubnailScrapper.register()
OuestFranceAnnonceScrapper.register()
OuestFranceScrapper.register()

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

