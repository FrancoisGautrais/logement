import datetime
import hashlib
import json
import time

import pytz
from django.db import models

# Create your models here.
from logement.libs import score
from logement.libs.score import score_debug
from logement.libs.scrapper.base.location_scrapper import ScrapRuntimeException
from logement.libs.scrapper.base.request import Request
from logement.libs.utils import find_domain, exception_to_string


class Annonce(models.Model):
    objects: models.Manager

    custom_id: str = models.TextField()
    site_id: str = models.TextField()
    title: str = models.TextField()
    content: str = models.TextField(blank=True, null=True)
    imgs: str = models.TextField(blank=True, null=True)
    address: str = models.TextField(blank=True, null=True)
    prix: float = models.FloatField(blank=True, null=True)
    surface: float = models.FloatField(blank=True, null=True)
    url: str = models.TextField(blank=True)
    phones: str = models.TextField(blank=True, null=True)
    data: str = models.TextField(blank=True, null=True)
    domain: str = models.CharField(max_length=255)
    creation_date: datetime.datetime = models.DateTimeField()
    score: int = models.IntegerField(default=0)
    is_relevant: bool = models.BooleanField(default=False)
    disable: bool = models.BooleanField(default=False)

    class Meta:
        unique_together = [['site_id', 'domain']]

    @classmethod
    def _prepare_dict(cls, data):
        data = {k: v for k, v in data.items()}
        data["site_id"] = data["custom_id"]
        data["custom_id"] = data["domain"] + ":" + data["custom_id"]
        data["phones"] = json.dumps(data.get("phones"))
        data["imgs"] = json.dumps(data.get("imgs"))
        data["data"] = json.dumps(data.get("data"))
        return data

    @classmethod
    def _create(cls, data):
        return cls(**cls._prepare_dict(data))

    @classmethod
    def create(cls, data):
        data["creation_date"] = datetime.datetime.now(tz=pytz.timezone("Europe/Paris"))
        data["score"] = score.score(data)
        data["is_relevant"] = score.is_relevant(data)
        return cls.objects.create(**cls._prepare_dict(data))

    @classmethod
    def exists(cls, data):
        data = cls._create(data)
        try:
            x = cls.objects.get(site_id=data.site_id, domain=data.domain)
            return True
        except cls.DoesNotExist:
            pass

        if data.address and data.prix and data.surface and len(
                cls.objects.filter(prix=data.prix, address=data.address, surface=data.surface)):
            return True

        if data.title and len(data.title.split(" ")) > 5 and len(cls.objects.filter(title=data.title)):
            return True
        return False

    @property
    def images(self):
        return json.loads(self.imgs)

    @property
    def image(self):
        if len(self.imgs) > 2:
            return self.images[0]

    @property
    def phone(self):
        phones = json.loads(self.phones)
        return " / ".join(phones)

    @property
    def adresse(self):
        return self.address if self.address else ""

    @property
    def age(self):
        seconds = time.time() - self.creation_date.timestamp()
        out = []
        d = seconds // (3600 * 24)
        if d:
            out.append(f"{int(d)} jours")
        h = (seconds % (3600 * 24)) // 3600
        m = (seconds // 3600) % 60
        out.append(f"{str(int(h)).zfill(2)} h")
        out.append(f"{str(int(m)).zfill(2)} m")

        return " ".join(out)

    @property
    def exclude(self):
        if not hasattr(self, "_exclude"):
            self._include, self._exclude = score_debug(self)
        return ", ".join(self._exclude)

    @property
    def include(self):
        if not hasattr(self, "_include"):
            self._include, self._exclude = score_debug(self)
        return ", ".join(self._include)

    def __repr__(self):
        return f"{self.id}, {self.surface} m?? {self.prix} ??? {self.domain} {self.address} {self.title}"

    def __str__(self):
        return self.__repr__()


class Filter(models.Model):
    value: str = models.TextField()
    type: str = models.TextField()
    score: int = models.IntegerField(default=1)

    @classmethod
    def load(cls, content, type):
        [cls.objects.create(value=line, type=type) for line in content.split("\n")]

    @classmethod
    def exclude(cls):
        return [x.value for x in cls.objects.filter(type="exclude")]

    @classmethod
    def include(cls):
        return [x.value for x in cls.objects.filter(type="include")]

    def __repr__(self):
        return f"{self.value};{self.type};{self.score}"

    def __str__(self):
        return self.__repr__()


class Options(models.Model):
    key: str = models.TextField(unique=True)
    value: str = models.TextField()

    @property
    def data(self):
        return json.loads(self.value)

    def set_value(self, data):
        self.value = json.dumps(data)
        self.save()
        return data

    @classmethod
    def get(cls, key):
        try:
            return cls.objects.get(key=key)
        except cls.DoesNotExist:
            return None


    @classmethod
    def get_value(cls, key, default=None):
        try:
            return json.loads(cls.objects.get(key=key).value)
        except cls.DoesNotExist:
            return default

    @classmethod
    def set(cls, key, value):
        try:
            return cls.objects.get(key=key).set_value(value)
        except cls.DoesNotExist:
            cls.objects.create(key=key, value=json.dumps(value))
            return value


class Error(models.Model):
    objects : models.Manager
    DoesNotExist : Exception

    first_date : datetime.datetime = models.DateTimeField()
    last_date : datetime.datetime = models.DateTimeField()
    url : datetime.datetime = models.TextField(null=True, blank=True)
    classe : str = models.TextField(null=True, blank=True)
    domain : str = models.TextField(null=True, blank=True)
    content : str = models.TextField()
    exception_type : str = models.CharField(max_length=128)
    checksum : str = models.TextField()

    class Meta:
        unique_together = [[ 'classe', 'checksum']]

    @classmethod
    def add(cls, exception, obj=None, url=None):
        now = datetime.datetime.now(tz=pytz.timezone("Europe/Paris"))
        domain = find_domain(url)
        url = url.url if isinstance(url, Request) else url
        classe = str(type(obj)) if object else None

        if isinstance(exception, ScrapRuntimeException):
            content = exception.content
            exception = exception.exception
        else:
            content = exception_to_string(exception)
        checksum = hashlib.sha512(content.encode("utf8")).hexdigest()

        try:
            data = cls.objects.get(checksum=checksum, classe=classe)
        except cls.DoesNotExist:
            data = None

        if data:
            data.last_date = now
            data.save()
        else:
            data = cls.objects.create(
                first_date=now,
                last_date=now,
                url=url,
                domain=domain,
                classe=classe,
                content=content,
                exception_type=type(exception).__name__,
                checksum=checksum
            )
        return data

    @classmethod
    def from_domain(cls, domain_or_url, **kwargs):
        if isinstance(domain_or_url, Request):
            domain_or_url = domain_or_url.url
        if domain_or_url and "/" in domain_or_url:
            domain_or_url = find_domain(domain_or_url)
        return cls.objects.filter(domain=domain_or_url, **kwargs).order_by("-last_date")



    @classmethod
    def last_from_domain(cls, domain_or_url):
        x = cls.from_domain(domain_or_url)
        if len(x):
            return x[0]
        else:
            return None



