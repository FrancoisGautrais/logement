import datetime
import json
import time

from django.db import models
from django.utils import timezone
import pytz

# Create your models here.
from logement.libs import score


class Annonce(models.Model):
    objects : models.Manager

    id : str  = models.TextField(primary_key=True)
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


    class Meta:
        unique_together = [['site_id', 'domain']]


    @classmethod
    def _prepare_dict(cls, data):
        data = {k:v for k,v in data.items()}
        data["site_id"]=data["id"]
        data["id"]=data["domain"]+":"+data["id"]
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



