import datetime
import json


from django.db import models


# Create your models here.
from logement.libs import score


class Annonce(models.Model):
    objects : models.Manager

    id : str  = models.TextField(primary_key=True)
    site_id: str = models.TextField()
    title : str  = models.TextField()
    content : str  = models.TextField(blank=True, null=True)
    imgs : list  = models.TextField(blank=True, null=True)
    address : str  = models.TextField(blank=True, null=True)
    prix : float  = models.FloatField(blank=True, null=True)
    surface : float  = models.FloatField(blank=True, null=True)
    url : str  = models.TextField(blank=True)
    phones : list = models.TextField(blank=True, null=True)
    data : dict = models.TextField(blank=True, null=True)
    domain : str = models.CharField(max_length=255)
    creation_date = models.DateTimeField()
    score = models.IntegerField(default=0)
    is_relevant = models.BooleanField(default=False)


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
        data["creation_date"]=datetime.datetime.now()
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



