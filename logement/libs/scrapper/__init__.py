from pathlib import Path
from logement.libs.scrapper.base.location_scrapper import ListScrapper, PageScrapper, ThumbnailScrapper

def import_module(x):
    module = __import__(x, fromlist=[f"{__name__}.sites"] )
    for name in  dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type):
            if issubclass(obj, ListScrapper):
                obj.register()
            elif issubclass(obj, ThumbnailScrapper):
                obj.register()
            elif issubclass(obj, PageScrapper):
                obj.register()
    return module



modules = [ import_module(f"{__name__}.sites.{x.name.split('.')[0]}") for x in (Path(__file__).parent / "sites").iterdir() if x.name.endswith(".py") ]



def scrap(url):
    return ListScrapper.scrap(url)