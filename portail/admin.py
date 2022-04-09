from django.contrib import admin

# Register your models here.
from portail.models import Annonce, Filter

admin.site.register(Filter)
admin.site.register(Annonce)