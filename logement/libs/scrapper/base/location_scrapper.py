import json
import re
import time

import requests


from logement.libs.scrapper.base.connector import HtmlConnector
from logement.libs.scrapper.base.helpers import BaseHelper, HelperHtmlText, HelperHtmlAttr, HelperJson
from logement.libs.scrapper.base.request import Get


class BadDomainException(Exception):
    pass


class UnhandledDomainException(Exception): pass

class ScrapRuntimeException(Exception):
    def __init__(self, exc, scrapper):
        self.exception=exc
        self.content=exception_to_string(exc)
        self.scrapper=str(scrapper)
        super().__init__(type(exc).__name__,exc)

import traceback
def exception_to_string(excp):
   stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=??
   pretty = traceback.format_list(stack)
   return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)


class BaseScrapper:
    NUMBER_REGEX=re.compile(r"(?P<number>\d+((\.|,)\d*)?)")
    REGEX_PHONE = re.compile("\d\d.?\d\d.?\d\d.?\d\d.?\d\d")
    CONNECTOR=HtmlConnector

    _SCRAPPERS=[]
    DOMAIN=None

    def __init__(self):
        self.connector=self.CONNECTOR()

    @classmethod
    def register(cls):
        if cls.DOMAIN is None:
            return
        ThumbnailScrapper._SCRAPPERS.append(cls)

    @classmethod
    def get_scrapper(cls, req, wanted_class, **kwargs):
            if isinstance(req, str):
                url=req
            else:
                url=req.url

            for classe in BaseScrapper._SCRAPPERS:
                if url.lower().startswith((f"https://{classe.DOMAIN}/", f"http://{classe.DOMAIN}/")) and issubclass(classe, wanted_class):
                    return classe
            return None


    def scrap(cls, **kwargs):
        raise NotImplementedError()


    def parseNumber(self, x):
        if x is None: return None
        if isinstance(x, (int,float)): return x
        val = re.findall(self.NUMBER_REGEX, x)
        for t in val:
            if len(t):
                c = t[0].replace(",",".")
                return float(c) if "." in c else int(c)
        return None

    def _call_auto(self, name, default=None):
        att = hasattr(self, f"QUERY_{name}") and getattr(self, f"QUERY_{name}")
        if att:
            if isinstance(att, BaseHelper):
                return att.get_value(self)
        return default

    @classmethod
    def find_phone(cls, data):
        ret = re.findall(cls.REGEX_PHONE, data)
        return ret

    @property
    def response(self):
        return self.request.response if hasattr(self, "request") and hasattr(self.request, "response") else None

    @property
    def response_text(self):
        x = self.response
        return x.text if x else None

    @property
    def response_bytes(self):
        x = self.response
        return x.content if x else None

    @property
    def response_json(self):
        x = self.response
        return json.loads(x.content) if x else None


    def clean_text(self, text):
        if isinstance(text, str):
            return text.rstrip(" \n\t").lstrip(" \n\t")



class LocationElemScrapper(BaseScrapper):
    QUERY_PRIX = None
    QUERY_CONTENT = None
    QUERY_ID = None
    QUERY_ADDRESS = None
    QUERY_SURFACE = None
    QUERY_TITLE = None
    QUERY_PHONES = None
    QUERY_IMGS = None

    def __init__(self, url=None, content=None, parent=None, **kwargs):
        super().__init__()
        self.parent = parent
        self.d = self.connector.from_request(url) if url else content
        self.glob = self.parent.d if self.parent else self.d
        self.data = self.init()
        self.custom_id = self.get_id()
        self.title = self.get_title()
        self.content = self.get_content()
        self.address = self.get_address()
        self.imgs = self.get_imgs()
        self.prix = self.parseNumber(self.get_prix())
        self.surface = self.parseNumber(self.get_surface())
        self.phones = self.get_phones()
        self.check_imgs()

    def check_imgs(self):
        out=[]
        for url in self.imgs:
            if url is None: continue
            if url.startswith(("data:", "http:", 'https:',)):
               out.append(url)
            else:
                out.append(f'https://{self.DOMAIN}{url}')
        self.imgs=out

    def get_id(self):
        x = self._call_auto("ID")
        if x: return x
        raise NotImplementedError()

    def get_title(self):
        return self._call_auto("TITLE")

    def get_address(self):
        return self._call_auto("ADDRESS")

    def get_content(self):
        return self._call_auto("CONTENT")

    def get_imgs(self):
        return self._call_auto("IMGS", [])

    def get_surface(self):
        return self._call_auto("SURFACE")

    def get_prix(self):
        return self._call_auto("PRIX")

    def get_phones(self):
        return self._call_auto("PHONES", [])

    def __call__(self, *args, **kwargs):
        return self.d.find(*args, **kwargs)

    def init(self):
        return self


    def as_dict(self):
        fields = [
            "prix", "phones", "surface", "imgs", "content", "title", "custom_id", "address", "url",

        ]
        x=  {k: getattr(self, k) for k in fields if hasattr(self, k)}
        x["domain"] = self.DOMAIN
        return x


class PageScrapper(LocationElemScrapper):
    def __init__(self, url, **kwargs):
        self.url=url
        super().__init__(url=url, **kwargs)

    @property
    def visited(self):
        return True

class ThumbnailScrapper(LocationElemScrapper):
    DOMAIN=None
    def __init__(self, d, parent):
        super().__init__(content=d, parent=parent)
        self.url = self.get_url()

    def get_url(self):
        return self._call_auto("URL")

    def visit(self):
        try:
            url = self.url
            if url is None:
                raise ValueError("Impossible de récupérer l'url de la page")
            x = self.get_scrapper(url, PageScrapper)
            return x(url=url, parent=self)
        except Exception as err:
            raise ScrapRuntimeException(err, self.__class__)

    @property
    def visited(self):
        return False

class ListScrapper(BaseScrapper):
    DOMAIN=None
    QUERY_ELEMENTS=None

    def __init__(self, request):
        super().__init__()
        if isinstance(request, str):
            request=Get(request)
        self.request = request
        self.url = request.url
        self.connector = self.CONNECTOR()
        if not re.match(rf"http(s)?://{self.DOMAIN}/.*", self.url):
            raise BadDomainException(self.DOMAIN, self.url)
        self.d = self.connector.from_request(self.request)
        self.elements=[]
        self.parse()

    def find_elements(self):
        if self.QUERY_ELEMENTS:
            return self.QUERY_ELEMENTS.get_value(self)
        raise NotImplementedError()

    def find_thubmnail_class(self):
        x = self.get_scrapper(self.url, wanted_class=ThumbnailScrapper)
        if x is None:
            UnhandledDomainException(f"No scrapper fot thubnail to domain '{self.url}'")
        return x


    def parse(self):
        data = self.find_elements()
        classe = self.find_thubmnail_class()
        if classe is None:
            raise UnhandledDomainException(f"Aucune classe pour scrapper les miniatures de l'url '{self.url}'")
        for x in data:
            self.elements.append(classe(self.connector.cast(x), self))


    def __call__(self, *args, **kwargs):
        return self.d(*args, **kwargs)


    @classmethod
    def scrap(cls, url):
        try:
            classe = cls.get_scrapper(url, ListScrapper)
            if classe is None:
                raise UnhandledDomainException(f"Aucune classe pour scrapper l'url '{url}'")
            return classe(url)
        except Exception as err:
            raise ScrapRuntimeException(err, cls)