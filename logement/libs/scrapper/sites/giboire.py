import json

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, PageScrapper, \
    HelperJson

url = "https://www.giboire.com/recherche-location/appartement/?address%5B%5D=RENNES&priceMin=500&priceMax=950&livingSurfaceMin=55&livingSurfaceMax=90&nbBedrooms%5B%5D=2&nbBedrooms%5B%5D=3&searchBy=undefined#both"



class GiboireAnnonceScrapper(PageScrapper):
    DOMAIN="www.giboire.com"
    QUERY_ID = HelperHtmlAttr(".estate", "data-id")
    QUERY_TITLE = HelperHtmlText(".presentation-bien_exclu_desc_type")
    QUERY_PRIX = HelperHtmlText(".presentation-bien_exclu_desc_prix")
    QUERY_CONTENT = HelperHtmlText(".descriptif-bien_description")
    QUERY_ADDRESS = HelperHtmlAttr(".map_giboire", "data-center")
    QUERY_SURFACE = HelperHtmlText(".presentation-bien_exclu_desc_dispo > p")


    def init(self):
        ret = {}
        for tr in self.d(".tab_informations > tr"):
                tds = tr.xpath("td")
                if len(tds)>1:
                    ret[tds[0].text]=self.clean_text(tds[1].text)
        return ret

    def get_phones(self):
        tel = self.d(".presentation-bien_contact_tel>a").text()
        if not tel: return None
        return self.find_phone(tel)

    def get_imgs(self):
        ret = []
        for x in self.d(".popin-slider_slide>img"):
            img = x.attrib.get('src')
            if img:
                ret.append(img)
        return ret

class GiboireThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.giboire.com"
    QUERY_TITLE =  HelperHtmlText(".card_title")
    QUERY_ID = HelperHtmlAttr(".card--list-mobile", "entityid")
    QUERY_PRIX = HelperHtmlText(".card_price")
    QUERY_URL = HelperHtmlAttr(".card_title", "href")



class GiboireScrapper(ListScrapper):
    DOMAIN="www.giboire.com"

    def find_elements(self):
        return [ x for x in self.d(".cards-carousel_item")]



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

