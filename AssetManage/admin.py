from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.AssetType)
admin.site.register(models.AssetTypeInfo)
admin.site.register(models.Asset)