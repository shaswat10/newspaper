from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.newsModel)
admin.site.register(models.sourceModel)