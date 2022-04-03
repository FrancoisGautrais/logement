


import requests
from pyquery import PyQuery as pq

from logement.libs.scrapper.base_scrapper import SiteScrapper, AnnonceScrapper

url = "https://www.ouestfrance-immo.com/louer/appartement--3-pieces_4-pieces/?lieux=100003,100013&prix=0_950"


class OuestFranceAnnonce(AnnonceScrapper):

    @classmethod
    def get_list(cls, obj):
        return obj(".annLink")

    def get_id(self):
        x = self.d
        print(type(x), self.d.xpath("div")[0].attrib)

class OuestFranceScrapper(SiteScrapper):
    DOMAIN="www.ouestfrance-immo.com"
    ANNONCE=OuestFranceAnnonce

x = SiteScrapper(url)
print(x.data)