import re

from pyquery import PyQuery as pq
class BadDomainException(Exception):
    pass
class AnnonceScrapper:
    _DOMAINS={}
    def __init__(self, d):
        self.d=d
        self.id = self.get_id()
        self.title = self.get_title()
        self.content = self.get_content()
        self.imgs = self.get_imgs()
        self.surface = self.get_surface()
        self.prix = self.get_prix()
        self.phone = self.get_phone()

    def get_id(self):
        raise NotImplementedError()

    def get_title(self):
        return ""

    def get_content(self):
        return ""

    def get_imgs(self):
        return []

    def get_surface(self):
        return 0.0

    def get_prix(self):
        raise NotImplementedError()

    def get_phone(self):
        return None

    @classmethod
    def get_list(cls, obj):
        return None

    def __call__(self, *args, **kwargs):
        return self.d.find(*args, **kwargs)


class SiteScrapper:

    _DOMAINS={}
    DOMAIN=None
    ANNONCE=None
    def __init__(self, url):
        self.url = url
        if not re.match(rf"https(s)?://{self.DOMAIN}/.*", self.url):
            raise BadDomainException(self.DOMAIN, url)
        self.d = pq(url=self.url)
        self.data=[]
        self.parse()

    def find_annonce(self):
        x = self.ANNONCE.get_list(self)
        if x: return x
        raise NotImplementedError()

    def parse(self):
        for x in self.find_annonce():
            self.data.append(self.ANNONCE(x))

    def scrap(self, url : str):
        for domain, classe in self._DOMAINS.items():
            if url.lower().startswith( (f"https://{domain}/", f"https://{domain}/"))
                return classe(url)
        return None


    def __call__(self, *args, **kwargs):
        return self.d(*args, **kwargs)