import json

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.helpers import HelperAttr, HelperJson
from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, PageScrapper

url = "https://www.ouestfrance-immo.com/louer/appartement--3-pieces_4-pieces/?lieux=100003,100013&prix=0_950"



class OuestFranceAnnonceScrapper(PageScrapper):
    DOMAIN="www.ouestfrance-immo.com"
    QUERY_ID = HelperHtmlAttr("#idAnnonce", "value")
    QUERY_PRIX = HelperHtmlAttr("#prix_reel", "value")
    QUERY_TITLE = HelperJson("mainEntity", "name")
    QUERY_CONTENT = HelperJson("mainEntity", "description")
    QUERY_IMGS = HelperJson("mainEntity", "photo", "contentUrl")
    QUERY_ADDRESS = HelperAttr("parent", "address")
    QUERY_SURFACE =  HelperAttr("parent", "surface")
    QUERY_PHONES =  HelperAttr("parent", "phones")


    def init(self):
        for x in self.d("script"):
            if x.attrib.get("type") == "application/ld+json":
                return json.loads(x.text)


class OuestFranceThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.ouestfrance-immo.com"
    QUERY_PRIX = HelperHtmlText(".annPrix")
    QUERY_TITLE = HelperHtmlText(".annTitre")
    QUERY_ADDRESS = HelperHtmlText(".annAdresse")
    QUERY_CONTENT = HelperHtmlText(".annTexte")
    QUERY_URL = HelperHtmlAttr(".annLink", "href", cast=lambda x: f"https://www.ouestfrance-immo.com{x}")
    QUERY_IMGS = HelperHtmlAttr(".annPhoto", "data-original", cast=lambda x: [x], )


    def get_surface(self):
        q = self.d(".annCriteres")
        for x in q:
            for div in x:
                for unit in div.xpath("span"):
                    if "m" in unit.text:
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

class OuestFranceScrapper(ListScrapper):
    DOMAIN="www.ouestfrance-immo.com"

    def find_elements(self):
        return [ x for x in self.d(".annLink") if x.attrib.get("data-trk-payload")]


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

