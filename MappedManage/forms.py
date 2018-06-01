#coding:utf-8
'''
Created on 2018年5月23日

@author: yuguanc
'''

from django.forms import ModelForm
from . import models
from django.forms import widgets
from django import forms

class Mapped_update_form(ModelForm):
    class Meta:
        model = models.Mapped
        fields = ['mapped_status','Domain','start_time','end_time','request_email','action_email',
                  'request_order','request_user','request_user_num','request_user_department','telephone','Mapped_description']
        widgets = {
                   'Domain':widgets.TextInput(attrs={'class':'form-control','placeholder':'域名'}),
                   'start_time':widgets.DateInput(attrs={'class':'layui-input date','placeholder':'yyyy-MM-dd','autocomplete':'off','lay-verify':'date'}),
                   'end_time':widgets.DateInput(attrs={'class':'layui-input date','placeholder':'yyyy-MM-dd','autocomplete':'off','lay-verify':'date'}),
                   'mapped_status':widgets.NullBooleanSelect(attrs={'class':'form-control','placeholder':'是否使用'}),
                   'request_email':widgets.TextInput(attrs={'class':'form-control','placeholder':'申请人邮箱'}),
                   'action_email':widgets.TextInput(attrs={'class':'form-control','placeholder':'操作人邮箱'}),
                   'request_order':widgets.TextInput(attrs={'class':'form-control','placeholder':'申请单号，可为空'}),
                   'request_user':widgets.TextInput(attrs={'class':'form-control','placeholder':'申请人员，可为空'}),
                   'request_user_num':widgets.TextInput(attrs={'class':'form-control','placeholder':'员工编号，可为空'}),
                   'request_user_department':widgets.TextInput(attrs={'class':'form-control','placeholder':'申请人部门，可为空'}),
                   'telephone':widgets.TextInput(attrs={'class':'form-control','placeholder':'申请人电话，可为空'}),
                   'Mapped_description':widgets.Textarea(attrs={'class':'form-control','placeholder':'备注信息，可为空'}),
                   }

        
        
class Mapped_edit_form(forms.Form):
    LANip = forms.CharField(label='内网IP',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'内网IP'}))
    LANPort = forms.CharField(label='内网端口',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'内网端口'}))
    WANip = forms.CharField(label='外网IP',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'外网IP'}))
    WANPort = forms.CharField(label='外网端口',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'外网端口'}))
    Domain = forms.CharField(required=False,label='域名',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'域名'}))
    start_time = forms.CharField(label='开启时间',max_length=75,widget=forms.DateInput(attrs={'class':'layui-input date','placeholder':'yyyy-MM-dd','autocomplete':'off','lay-verify':'date'}))
    end_time = forms.CharField(label='关闭时间',max_length=75,widget=forms.DateInput(attrs={'class':'layui-input date','placeholder':'yyyy-MM-dd','autocomplete':'off','lay-verify':'date'}))
    request_email = forms.CharField(label='申请人邮箱',max_length=75,widget=forms.EmailInput(attrs={'class':'layui-input','placeholder':'申请人邮箱'}))
    action_email = forms.CharField(label='操作人邮箱',max_length=75,widget=forms.EmailInput(attrs={'class':'layui-input','placeholder':'操作人邮箱'}))
    request_order = forms.CharField(required=False,label='申请单号',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'申请单号，可为空'}))
    request_user = forms.CharField(required=False,label='申请人',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'申请人员，可为空'}))
    request_user_num = forms.CharField(required=False,label='员工编号',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'员工编号，可为空'}))
    request_user_department = forms.CharField(required=False,label='申请部门',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'申请人部门，可为空'}))
    telephone = forms.CharField(required=False,label='联系电话',max_length=75,widget=forms.TextInput(attrs={'class':'layui-input','placeholder':'申请人电话，可为空'}))
    Mapped_description = forms.CharField(required=False,label='映射简介',max_length=500,widget=forms.Textarea(attrs={'class':'layui-input','placeholder':'备注信息，可为空'}))
    