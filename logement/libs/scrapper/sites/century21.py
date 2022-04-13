import json
import re

import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base.helpers import HelperHtml, HelperAttr, HelperConst
from logement.libs.scrapper.base.location_scrapper import ListScrapper, ThumbnailScrapper, HelperHtmlText, HelperHtmlAttr, PageScrapper, \
    HelperJson

DOMAIN="www.century21.fr"
url = "https://www.century21.fr/annonces/f/location-appartement/cpv-35000_rennes/s-55-90/st-0-/b-0-950/p-3-4/"



class Century21AnnonceScrapper(PageScrapper):
    DOMAIN=DOMAIN
    QUERY_TITLE = HelperAttr("parent", "title")
    QUERY_CONTENT = HelperHtmlText(".has-formated-text")
    QUERY_ID = HelperAttr("parent", "custom_id")
    QUERY_PRIX = HelperAttr("parent", "prix")
    QUERY_SURFACE = HelperAttr("parent", "surface")
    QUERY_IMGS = HelperHtmlAttr("img.c-the-slider__slide__img", ("src", "data-src"), join=None)

    def get_phones(self):
        for x in self.d(".tw-flex-grow>a"):
            tel = x.attrib.get("data-click-label")
            if tel:
                return self.find_phone(tel)
        return []


class Century21ThubnailScrapper(ThumbnailScrapper):
    DOMAIN=DOMAIN
    QUERY_TITLE =  HelperHtmlText(".tw-text-c21-gold-darker")
    QUERY_ID = HelperHtmlAttr(".c-the-property-thumbnail-with-content", "data-uid")
    QUERY_PRIX = HelperHtmlText("div.tw-mt-4>div.c-text-theme-heading-1")
    QUERY_URL = HelperConst("https://www.century21.fr")+HelperHtmlAttr("a.c-the-button", "href")
    QUERY_SURFACE=HelperHtmlText("div.tw-bg-c21-grey-light>div>div.c-text-theme-heading-4", regex=re.compile(r"(?P<name>\d+)\s*m"))




class Century21Scrapper(ListScrapper):
    DOMAIN=DOMAIN
    QUERY_ELEMENTS = HelperHtml(".js-the-list-of-properties-list-property")



if __name__ == "__main__":
    from logement.libs.scrapper import scrap
    x = scrap(url)
    for v in x.elements:
        d = v.visit()
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

