import datetime
import json
import time
from pathlib import Path

from django.db import models
from django.utils import timezone
import pytz

# Create your models here.
from logement.libs import score
from logement.libs.score import score_debug


class Annonce(models.Model):
    objects : models.Manager

    custom_id : str  = models.TextField()
    site_id: str = models.TextField()
    title : str  = models.TextField()
    content : str  = models.TextField(blank=True, null=True)
    imgs : str  = models.TextField(blank=True, null=True)
    address : str  = models.TextField(blank=True, null=True)
    prix : float  = models.FloatField(blank=True, null=True)
    surface : float  = models.FloatField(blank=True, null=True)
    url : str  = models.TextField(blank=True)
    phones : str = models.TextField(blank=True, null=True)
    data : str = models.TextField(blank=True, null=True)
    domain : str = models.CharField(max_length=255)
    creation_date : datetime.datetime = models.DateTimeField()
    score : int = models.IntegerField(default=0)
    is_relevant : bool = models.BooleanField(default=False)
    disable : bool  = models.BooleanField(default=False)


    class Meta:
        unique_together = [['site_id', 'domain']]


    @classmethod
    def _prepare_dict(cls, data):
        data = {k:v for k,v in data.items()}
        data["site_id"]=data["custom_id"]
        data["custom_id"]=data["domain"]+":"+data["custom_id"]
        data["phones"]=json.dumps(data.get("phones"))
        data["imgs"]=json.dumps(data.get("imgs"))
        data["data"]=json.dumps(data.get("data"))
        return data

    @classmethod
    def _create(cls, data):
        return cls(**cls._prepare_dict(data))

    @classmethod
    def create(cls, data):
        data["creation_date"]=datetime.datetime.now(tz=pytz.UTC)
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

        if data.address and data.prix and data.surface and len(cls.objects.filter(prix=data.prix, address=data.address, surface=data.surface)):
                return True

        if data.title and len(data.title.split(" "))>5 and len(cls.objects.filter(title=data.title)):
            return True
        return False

    @property
    def images(self):
        return json.loads(self.imgs)

    @property
    def image(self):
        if len(self.imgs)>2:
            return self.images[0]


    @property
    def phone(self):
        phones=json.loads(self.phones)
        return " / ".join(phones)


    @property
    def adresse(self):
        return self.address if self.address else ""


    @property
    def age(self):
        seconds = time.time() - self.creation_date.timestamp()
        out=[]
        d = seconds // (3600*24)
        if d:
            out.append(f"{int(d)} jours")
        h  = seconds // 3600
        m  = (seconds // 3600) % 60
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
        return f"{self.id}, {self.surface} m² {self.prix} € {self.domain} {self.address} {self.title}"

    def __str__(self):
        return self.__repr__()

class Filter(models.Model):

    value : str = models.TextField()
    type : str = models.TextField()
    score : int = models.IntegerField(default=1)


    @classmethod
    def load(cls, content, type):
        data = content.split("\n")
        for line in data:
            cls.objects.create(value = line, type=type)


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