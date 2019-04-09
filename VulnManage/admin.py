from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.Advance_vulns)
admin.site.register(models.Cnvdfiles)
admin.site.register(models.Vulnerability)
