#coding:utf-8
from django.contrib import admin
from . import models

# Register your models here.
# Register your models here.
class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('article_type_name','article_type_body')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_name','article_updatetime')
    
admin.site.register(models.ArticleType,ArticleTypeAdmin)
admin.site.register(models.Article,ArticleAdmin)