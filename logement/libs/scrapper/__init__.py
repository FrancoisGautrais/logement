from pathlib import Path
from logement.libs.scrapper.base.location_scrapper import ListScrapper
modules = [ __import__(f"{__name__}.sites.{x.name.split('.')[0]}") for x in (Path(__file__).parent / "sites").iterdir() if x.name.endswith(".py") ]


def scrap(url):
    return ListScrapper.scrap(url)