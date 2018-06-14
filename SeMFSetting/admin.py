#coding:utf-8
from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Scanner)
admin.site.register(models.ScannerPolicies)
admin.site.register(models.files)