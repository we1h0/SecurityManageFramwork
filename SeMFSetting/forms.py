#coding:utf-8
'''
Created on 2018年6月8日

@author: yuguanc
'''
from . import models
from django.forms import ModelForm,widgets

class File(ModelForm):
    class Meta:
        model = models.files
        fields=['name','file_type','file']
        widgets ={
            'name':widgets.TextInput(attrs={'class':'form-control','placeholder':'文件名称'}),
            'file_type':widgets.Select(attrs={'class':'form-control','placeholder':'文件类型'}),
            'file':widgets.FileInput(),
            }