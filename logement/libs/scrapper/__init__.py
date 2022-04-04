from logement.libs.scrapper.location_scrapper import ListScrapper
from logement.libs.scrapper.ouest_france import OuestFranceThubnailScrapper
from logement.libs.scrapper.ouest_france import OuestFranceScrapper


def scrap(url, **kwargs):
    return ListScrapper.scrap(url)