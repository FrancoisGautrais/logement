import json
from pathlib import Path

import requests
from logement.libs import scrapper
from logement.libs.scrapper.base.connector import JsonConnector
from logement.libs.scrapper.base.location_scrapper import PageScrapper, AutoText, AutoAttr, AutoData, ThumbnailScrapper, ListScrapper

url = "https://www.bienici.com/realEstateAds.json?filters=%7B%22size%22%3A24%2C%22from%22%3A0%2C%22showAllModels%22%3Afalse%2C%22filterType%22%3A%22rent%22%2C%22propertyType%22%3A%5B%22flat%22%5D%2C%22minPrice%22%3A600%2C%22maxPrice%22%3A950%2C%22minRooms%22%3A3%2C%22maxRooms%22%3A4%2C%22minArea%22%3A55%2C%22maxArea%22%3A90%2C%22page%22%3A1%2C%22sortBy%22%3A%22relevance%22%2C%22sortOrder%22%3A%22desc%22%2C%22onTheMarket%22%3A%5Btrue%5D%2C%22zoneIdsByTypes%22%3A%7B%22zoneIds%22%3A%5B%22-54517%22%5D%7D%7D&extensionType=extendedIfNoResult"

class BienIciThubnailScrapper(ThumbnailScrapper):
    CONNECTOR = JsonConnector
    DOMAIN="www.bienici.com"
    QUERY_TITLE =  AutoData("id")
    QUERY_ID = AutoData("id")
    QUERY_PRIX = AutoData("price")
    QUERY_CONTENT = AutoData("description")
    QUERY_ADDRESS = AutoData("district", "name")
    QUERY_SURFACE = AutoData('surfaceArea')

    def get_url(self):
        return f"https://{self.DOMAIN}/annonce/location/{self._city}/{self._nb_pieces}pieces/{self.id}"

    def visit(self):
        return self

    def init(self):
        self._city=self.d["city"]
        self._nb_pieces = self.d["roomsQuantity"]
        return self.d


    def get_imgs(self):
        return [
            x.get("url_photo") for x in self.data.get("photos", [])
        ]

class BienIciScrapper(ListScrapper):
    CONNECTOR = JsonConnector
    DOMAIN="www.bienici.com"
    CAST = lambda x: x
    READ_FCT = lambda *args, **kwargs: json.loads(requests.get(kwargs.get('url')).content)

    def find_elements(self):
        return self.d["realEstateAds"]


BienIciThubnailScrapper.register()
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


