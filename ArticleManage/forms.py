#coding:utf-8
'''
Created on 2018年5月22日

@author: yuguanc
'''



from django.forms import ModelForm
from . import models
from django.forms import widgets

class Article_edit_form(ModelForm):
    class Meta:
        model = models.Article
        fields = ['article_name','article_type','article_body','file']
        widgets = {
                   'article_name':widgets.TextInput(attrs={'class':'form-control','placeholder':'文章名称'}),
                   'article_type':widgets.Select(attrs={'class':'form-control'}),
                   'article_body':widgets.Textarea(attrs={'class':'form-control','placeholder':'知识库内容'}),
                   'file':widgets.FileInput(),
                   }
        
class Article_comment_edit_form(ModelForm):
    class Meta:
        model = models.ArticleComments
        fields = ['article_comment_body']
        widgets = {
                   'article_comment_body':widgets.TextInput(attrs={'class':'form-control'}),
                   }