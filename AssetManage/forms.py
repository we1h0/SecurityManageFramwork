#coding:utf-8
'''
Created on 2018年5月15日

@author: yuguanc
'''
from . import models
from django import forms
from django.forms import ModelForm,widgets


class HandoverActionForm(ModelForm):
    class Meta:
        model = models.Handover
        fields = ['action_reason']
        widgets = {
                   'action_reason':widgets.Textarea(attrs={'class':'form-control','placeholder':'资产交接审批说明'}),
                   }

class HandoverForm(ModelForm):
    class Meta:
        model = models.Handover
        fields = ['dst_email','reason']
        widgets = {
                   'dst_email':widgets.TextInput(attrs={'class':'form-control','placeholder':'请输入对方账号邮箱'}),
                   'reason':widgets.Textarea(attrs={'class':'form-control','placeholder':'资产转让说明（该操作会将您名下的资产转让 给目标账号，并停用该账号，请谨慎操作）'}),
                   }



class AssetUserForm(ModelForm):
    class Meta:
        model = models.AssetUser
        fields = ['dst_user_email','reason','asset_list']
        widgets = {
                   'dst_user_email':widgets.TextInput(attrs={'class':'form-control','placeholder':'请输入对方账号邮箱'}),
                   'reason':widgets.Textarea(attrs={'class':'form-control','placeholder':'该操作会将本网段所有资产添加至对方名下，请谨慎操作'}),
                   'asset_list':widgets.TextInput(attrs={'class':'form-control','placeholder':'资产列表','type':'hidden'}),
                   }



class Asset_create_form(ModelForm):
    class Meta:
        model = models.Asset
        fields=['asset_name','asset_type','asset_key','asset_out_id','asset_area','user_email','asset_description']
        widgets ={
            'asset_name':widgets.TextInput(attrs={'class':'form-control','placeholder':'资产名称'}),
            'asset_type':widgets.Select(attrs={'class':'form-control','placeholder':'资产类型'}),
            'asset_key':widgets.TextInput(attrs={'class':'form-control','placeholder':'资产标识/服务器为ip，网站为域名或访问地址,APP为应用名称'}),
            'asset_area':widgets.Select(attrs={'class':'form-control','placeholder':'资产属地'}),
            'user_email':widgets.TextInput(attrs={'class':'form-control','placeholder':'请填写资产使用者邮箱，默认为申请人员邮箱'}),
            'asset_out_id':widgets.TextInput(attrs={'class':'form-control','placeholder':'资产原始编号，如无，可不填'}),
            'asset_description':widgets.Textarea(attrs={'class':'form-control','placeholder':'资产描述'}),
            }
        
        
class AssetRequest_edit_form(ModelForm):
    class Meta:
        model = models.AssetRequest
        fields = ['asset_key','asset_type','request_action','request_reason']
        widgets = {
                   'asset_key':widgets.TextInput(attrs={'class':'form-control','placeholder':'填写操作目标IP/url/md5'}),
                   'asset_type':widgets.Select(attrs={'class':'form-control','placeholder':'资产类型'}),
                   'request_action':widgets.Select(attrs={'class':'form-control','placeholder':'操作类型'}),
                   'request_reason':widgets.Textarea(attrs={'class':'form-control','placeholder':'申请理由'}),
                   }
        
class Asset_port_info(ModelForm):
    class Meta:
        model = models.Port_Info
        fields=['port','name','product','version','port_info']
        widgets ={
            'name':widgets.TextInput(attrs={'class':'form-control','placeholder':'服务名称'}),
            'port':widgets.TextInput(attrs={'class':'form-control','placeholder':'开放端口'}),
            'product':widgets.TextInput(attrs={'class':'form-control','placeholder':'对应服务'}),
            'version':widgets.TextInput(attrs={'class':'form-control','placeholder':'应用版本'}),
            'port_info':widgets.Textarea(attrs={'class':'form-control','placeholder':'端口介绍'}),
            }
        
class Asset_plugin_info(ModelForm):
    class Meta:
        model = models.Plugin_Info
        fields=['name','version','plugin_info']
        widgets ={
            'name':widgets.TextInput(attrs={'class':'form-control','placeholder':'插件名称'}),
            'version':widgets.TextInput(attrs={'class':'form-control','placeholder':'插件版本'}),
            'plugin_info':widgets.TextInput(attrs={'class':'form-control','placeholder':'插件说明'}),
            }
        
class File_info(ModelForm):
    class Meta:
        model = models.File
        fields=['name','file','file_info']
        widgets ={
            'name':widgets.TextInput(attrs={'class':'form-control','placeholder':'文件名称'}),
            'file':widgets.FileInput(),
            'file_info':widgets.Textarea(attrs={'class':'form-control','placeholder':'简述附件内容'}),
            }     
        
class Asset_connect_form(forms.Form):
    asset_key = forms.CharField(label='资产标识',widget = forms.TextInput(attrs={'class':'form-control','placeholder':'资产标识/服务器为ip，网站为域名或访问地址'}))


class OS_Info_form(ModelForm):
    class Meta:
        model = models.OS_Info
        fields=['hostname','os','cpu_model','cpu_num','memory','disk','monitor','vendor','sn','cabinet','up_time','guarante_time','down_time']
        widgets ={
            'hostname':widgets.TextInput(attrs={'class':'form-control','placeholder':'主机hostname'}),
            'os':widgets.TextInput(attrs={'class':'form-control','placeholder':'操作系统'}),
            'vendor':widgets.TextInput(attrs={'class':'form-control','placeholder':'设备厂商'}),
            'cpu_model':widgets.TextInput(attrs={'class':'form-control','placeholder':'CPU类型'}),
            'cpu_num':widgets.TextInput(attrs={'class':'form-control','placeholder':'CPU数量'}),
            'memory':widgets.TextInput(attrs={'class':'form-control','placeholder':'内存大小'}),
            'disk':widgets.TextInput(attrs={'class':'form-control','placeholder':'磁盘大小'}),
            'monitor':widgets.TextInput(attrs={'class':'form-control','placeholder':'监控关联'}),
            'sn':widgets.TextInput(attrs={'class':'form-control','placeholder':'SN号'}),
            'cabinet':widgets.TextInput(attrs={'class':'form-control','placeholder':'机房/机柜信息'}),
            'up_time':widgets.DateInput(attrs={'class':'layui-input date','placeholder':'yyyy-MM-dd','autocomplete':'off','lay-verify':'date'}),
            'guarante_time':widgets.DateInput(attrs={'class':'layui-input date','placeholder':'yyyy-MM-dd','autocomplete':'off','lay-verify':'date'}),
            'down_time':widgets.DateInput(attrs={'class':'layui-input date','placeholder':'yyyy-MM-dd','autocomplete':'off','lay-verify':'date'}),
            }
        
        
class Internet_Info_form(ModelForm):
    class Meta:
        model = models.Internet_Info
        fields=['middleware','middleware_version','is_out','out_key','web_status','language','language_version','web_framwork','web_framwork_version']
        widgets ={
            'middleware':widgets.TextInput(attrs={'class':'form-control','placeholder':'中间件'}),
            'middleware_version':widgets.TextInput(attrs={'class':'form-control','placeholder':'中间件版本'}),
            'is_out':widgets.NullBooleanSelect(attrs={'class':'form-control','placeholder':'是否发布'}),
            'out_key':widgets.TextInput(attrs={'class':'form-control','placeholder':'外网域名'}),
            'web_status':widgets.Select(attrs={'class':'form-control','placeholder':'状态说明'}),
            'language':widgets.Select(attrs={'class':'form-control','placeholder':'开发语言'}),
            'language_version':widgets.TextInput(attrs={'class':'form-control','placeholder':'语言版本'}),
            'web_framwork':widgets.TextInput(attrs={'class':'form-control','placeholder':'开发框架'}),
            'web_framwork_version':widgets.TextInput(attrs={'class':'form-control','placeholder':'框架版本'}),
            }