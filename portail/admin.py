from django.contrib import admin

# Register your models here.
from portail.models import Annonce, Filter, Error, Options

admin.site.register(Filter)
admin.site.register(Annonce)
admin.site.register(Error)
admin.site.register(Options)