import json

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, PageScrapper, \
    HelperJson

url = "https://www.blot-immobilier.fr/habitat/location/appartement--appartement-neuf/ille-et-vilaine/rennes/?t3=true&t4=true&page=1&tri=nouveaute"



class BlotAnnonceScrapper(PageScrapper):
    DOMAIN="www.blot-immobilier.fr"
    QUERY_TITLE = HelperHtmlText("h1")
    QUERY_CONTENT = HelperHtmlText("#descriptif")
    QUERY_ADDRESS = HelperJson("Secteur")
    QUERY_ID = HelperHtmlText("small")
    QUERY_IMGS = HelperHtmlAttr(".gallery>img", "src", cast=lambda x : [x])
    QUERY_PRIX = HelperHtmlText(".prix>strong")
    QUERY_SURFACE = HelperJson("Surface habitable")


    def init(self):
        ret = {}
        for tr in self.d(".tab_informations > tr"):
                tds = tr.xpath("td")
                if len(tds)>1:
                    ret[tds[0].text]=self.clean_text(tds[1].text)
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
        tel = self.d(".btn_tel").attr("data-tel")
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
                ret.append(img)

        return ret

class BlotThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.blot-immobilier.fr"
    QUERY_TITLE =  HelperHtmlText(".ref")
    QUERY_ID = HelperHtmlText(".ref")
    QUERY_PRIX = HelperHtmlText(".prix>strong")
    QUERY_URL = HelperHtmlAttr("a", "href", cast=lambda x: f"https://www.blot-immobilier.fr{x}")



class BlotScrapper(ListScrapper):
    DOMAIN="www.blot-immobilier.fr"

    def find_elements(self):
        return [ x for x in self.d(".search_results > .container > .bloc_annonce")]


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

