import json

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, PageScrapper, \
    HelperJson

url = "https://www.pigeaultimmobilier.com/location/?sous-categorie%5B%5D=1455&agences%5B%5D=26548&prix_min=500&prix_max=950&submitted=1&o=date-desc&action=load_search_results&wia_6_type=location&searchOnMap=0&wia_1_reference="



class PigeaultAnnonceScrapper(PageScrapper):
    DOMAIN="www.pigeaultimmobilier.com"
    QUERY_ID = HelperHtmlAttr(".estate", "data-id")
    QUERY_TITLE = HelperHtmlText("#contenu > h2 > span")
    QUERY_PRIX = HelperHtmlText(".prix")
    QUERY_CONTENT = HelperHtmlText("#contenu > p")
    QUERY_ADDRESS = HelperHtmlText("small.h6")
    QUERY_SURFACE = HelperHtmlText(".surface")
    QUERY_PHONES = HelperHtmlAttr("#phone-top", "data-number", cast=lambda x: [x])

    def get_id(self):
        for x in self.d("article"):
            return x.attrib.get("id")

    def get_imgs(self):
        ret = []
        for x in self.d("figure>a>img"):
            img = x.attrib.get('data-lazy', x.attrib.get('data-src'))
            if img:
                ret.append(img)
        return ret

class PigeaultThubnailScrapper(ThumbnailScrapper):
    DOMAIN="www.pigeaultimmobilier.com"
    QUERY_TITLE =  HelperHtmlAttr("img", "alt")
    QUERY_ID = HelperHtmlAttr("article", "id")
    QUERY_PRIX = HelperHtmlText(".prix")
    QUERY_URL = HelperHtmlAttr("article>div>a", "href")



class PigeaultScrapper(ListScrapper):
    DOMAIN="www.pigeaultimmobilier.com"

    def find_elements(self):
        return [ x for x in self.d("article")]


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

