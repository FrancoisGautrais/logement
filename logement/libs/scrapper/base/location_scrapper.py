import re
import time

import requests

from logement.libs.scrapper.base.connector import HtmlConnector


class BadDomainException(Exception):
    pass


class UnhandledDomainException(Exception): pass



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
            raise ValueError("Le domain n'est pas défini")
        ThumbnailScrapper._SCRAPPERS.append(cls)

    @classmethod
    def get_scrapper(cls, url, wanted_class, **kwargs):
            for classe in BaseScrapper._SCRAPPERS:
                if url.lower().startswith((f"https://{classe.DOMAIN}/", f"https://{classe.DOMAIN}/")) and issubclass(classe, wanted_class):
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
            if isinstance(att, AutoData):
                return att.get_value(self.data)
            if hasattr(self, att.FUNCTION):
                x =  getattr(self, att.FUNCTION)(att.data, *att.params, fct=att.cast)
                return x
        return default

    @classmethod
    def find_phone(cls, data):
        ret = re.findall(cls.REGEX_PHONE, data)
        return ret

class Auto:
    FUNCTION=None
    def __init__(self, d, *params, cast=None):
        self.data = d
        self.params = params
        self.cast = cast


class AutoText(Auto):
    FUNCTION="_text"


class AutoAttr(Auto):
    FUNCTION="_attr"


class AutoData(Auto):
    FUNCTION="_data"

    def __init__(self, *params, cast=None):
        super().__init__(None, *params, cast)

    def get_value(self, x):
        curr = x
        for key in self.params:
            if key is None: continue
            if isinstance(key, int) and isinstance(curr, list):
                if key>=len(curr): return None
                curr=curr[key]
            elif isinstance(curr, dict):
                if key not in curr: return None
                curr=curr[key]
            else:
                return None
        return curr

class ElementScrapper(BaseScrapper):

    def __init__(self, url=None, content=None, parent=None):
        super().__init__()
        self.parent = parent
        self.d = self.connector.from_request(url) if url else content
        self.glob = self.parent.d if self.parent else self.d

    def _text(self, query, fct=None, root=None):
        root = root or "d"
        if not hasattr(self, root): return None
        x = getattr(self, root)(query)
        if x: return x.text() if fct is None else fct(x.text())
        return None

    def _attr(self, query, attr, fct=None, root=None):
        root = root or "d"
        if not hasattr(self, root): return None
        for x in getattr(self, root)(query):
            val = x.attrib.get(attr)
            if val is None: return None
            return fct(val) if fct else val

    def clean_text(self, text):
        if isinstance(text, str):
            return text.rstrip(" \n\t").lstrip(" \n\t")

class LocationElemScrapper(ElementScrapper):
    QUERY_PRIX = None
    QUERY_CONTENT = None
    QUERY_ID = None
    QUERY_ADDRESS = None
    QUERY_SURFACE = None
    QUERY_TITLE = None
    QUERY_PHONES = None
    QUERY_IMGS = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = self.init()
        self.id = self.get_id()
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
            "prix", "phones", "surface", "imgs", "content", "title", "id", "address", "url",

        ]
        x=  {k: getattr(self, k) for k in fields if hasattr(self, k)}
        x["domain"] = self.DOMAIN
        return x


class PageScrapper(LocationElemScrapper):
    def __init__(self, url):
        super().__init__(url=url)

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
        url = self.url
        if url is None:
            raise ValueError("Impossible de récupérer l'url de la page")
        x = self.get_scrapper(url, PageScrapper)
        return x(url=url)

    @property
    def visited(self):
        return False


class ListScrapper(BaseScrapper):
    DOMAIN=None
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.connector = self.CONNECTOR()
        if not re.match(rf"https(s)?://{self.DOMAIN}/.*", self.url):
            raise BadDomainException(self.DOMAIN, url)
        self.d = self.connector.from_request(self.url)
        self.data=[]
        self.parse()

    def find_elements(self):
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
            self.data.append(classe(self.connector.cast(x), self))


    def __call__(self, *args, **kwargs):
        return self.d(*args, **kwargs)


    @classmethod
    def scrap(cls, url):
        classe = cls.get_scrapper(url, ListScrapper)
        if classe is None:
            raise UnhandledDomainException(f"Aucune classe pour scrapper l'url '{url}'")
        return classe(url)