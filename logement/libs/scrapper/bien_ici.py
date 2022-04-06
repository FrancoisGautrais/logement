import json
from pathlib import Path

import requests

from logement.libs.scrapper import ListScrapper
from logement.libs.scrapper.location_scrapper import PageScrapper, AutoText, AutoAttr, AutoData, ThumbnailScrapper

url = "https://www.bienici.com/realEstateAds.json?filters=%7B%22size%22%3A24%2C%22from%22%3A0%2C%22showAllModels%22%3Afalse%2C%22filterType%22%3A%22rent%22%2C%22propertyType%22%3A%5B%22flat%22%5D%2C%22minPrice%22%3A600%2C%22maxPrice%22%3A950%2C%22minRooms%22%3A3%2C%22maxRooms%22%3A4%2C%22minArea%22%3A55%2C%22maxArea%22%3A90%2C%22page%22%3A1%2C%22sortBy%22%3A%22relevance%22%2C%22sortOrder%22%3A%22desc%22%2C%22onTheMarket%22%3A%5Btrue%5D%2C%22zoneIdsByTypes%22%3A%7B%22zoneIds%22%3A%5B%22-54517%22%5D%7D%7D&extensionType=extendedIfNoResult&leadingCount=2"



class BienIciAnnonceScrapper(PageScrapper):
    DOMAIN="www.bienici.com"
    QUERY_TITLE = AutoText("h1")
    QUERY_CONTENT = AutoText("#descriptif")
    QUERY_ADDRESS = AutoText(".adresse")
    QUERY_ID = AutoText("small")
    QUERY_IMGS = AutoAttr(".gallery>img", "src", cast=lambda x : [x])
    QUERY_PRIX = AutoText(".prix>strong")
    QUERY_SURFACE = AutoData("Surface habitable")


    def init(self):
        ret = {}
        for tr in self.d(".tab_informations > tr"):
                tds = tr.xpath("td")
                if len(tds)>1:
                    ret[tds[0].text]=self.clean_text(tds[1].text)
        print(ret)
        return ret

    def get_prix(self):
        numbers = "0123456789"
        loyer_hc = "".join([x for x in self.data.get("Loyer HC", "") if x in numbers])
        provision = "".join([x for x in self.data.get("Provisions charges/mois", "") if x in numbers])

        if not loyer_hc:
            return None
        acc = int(loyer_hc)
        if provision:
            acc+=int(provision)
        return acc


    def get_phones(self):
        tel = self._attr(".btn_tel", "data-tel")
        if not tel: return None
        tel = tel.split("'")
        if len(tel) == 3:
            return self.find_phone(tel[1])
        return None

    def get_imgs(self):
        ret = []
        for x in self.d(".gallery>img"):
            img = x.attrib.get('src')
            if img:
                ret.append(f"https://www.blot-immobilier.fr/{img}")

        return ret

class BienIciThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.bienici.com"
    QUERY_TITLE =  AutoText(".ref")
    QUERY_ID = AutoText(".ref")
    QUERY_PRIX = AutoText(".prix>strong")
    QUERY_URL = AutoAttr("a", "href", cast=lambda x: f"https://www.blot-immobilier.fr{x}")

    def init(self):
        self.data=self.d

def ident(x)

class BienIciScrapper(ListScrapper):
    DOMAIN="www.bienici.com"
    CAST = lambda x: x
    READ_FCT = lambda *args, **kwargs: json.loads(requests.get(kwargs.get('url')).content)
    def find_elements(self):
        return self.d["realEstateAds"]


BienIciThubnailScrapper.register()
BienIciAnnonceScrapper.register()
BienIciScrapper.register()

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


