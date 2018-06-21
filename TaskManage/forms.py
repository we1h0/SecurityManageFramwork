#coding:utf-8
'''
Created on 2018年5月25日

@author: yuguanc
'''

from . import models
from django.forms import ModelForm
from django.forms import widgets



class TaskSyncForm(ModelForm):
    class Meta:
        model = models.Task
        fields = ['task_name','task_scanner','scan_id','task_targetinfo']
        widgets = {
                   'task_name':widgets.TextInput(attrs={'class':'form-control','placeholder':'任务名称，一般以系统名称+版本+日期'}),
                   'scan_id':widgets.TextInput(attrs={'class':'form-control','placeholder':'扫描器对应的任务标识,当前只支持nessus'}),
                   'task_scanner':widgets.Select(attrs={'class':'form-control','placeholder':'扫描节点'}),
                   'task_targetinfo':widgets.Textarea(attrs={'class':'form-control','placeholder':'本次任务说明，如漏洞复查，周期检查、版本更新、上线准备等'}),
                   }
        
        
class TaskCreateForm(ModelForm):
    class Meta:
        model = models.Task
        fields = ['task_name','scanner_police','task_target','task_targetinfo']
        widgets = {
                   'task_name':widgets.TextInput(attrs={'class':'form-control','placeholder':'任务名称，一般以系统名称+版本+日期'}),
                   #'task_scanner':widgets.Select(attrs={'class':'form-control','placeholder':'扫描节点'}),
                   'scanner_police':widgets.Select(attrs={'class':'form-control','placeholder':'扫描策略'}),
                   'task_target':widgets.TextInput(attrs={'class':'form-control','placeholder':'扫描目标,ip/url'}),
                   'task_targetinfo':widgets.Textarea(attrs={'class':'form-control','placeholder':'本次任务说明，如漏洞复查，周期检查、版本更新、上线准备等'}),
                   }
        
class TaskScanForm(ModelForm):
    class Meta:
        model = models.Task
        fields = ['task_name','scanner_police','task_target','task_targetinfo']
        widgets = {
                   'task_name':widgets.TextInput(attrs={'class':'form-control','placeholder':'任务名称，一般以系统名称+版本+日期'}),
                   #'task_scanner':widgets.Select(attrs={'class':'form-control','placeholder':'扫描节点'}),
                   'scanner_police':widgets.Select(attrs={'class':'form-control','placeholder':'扫描策略'}),
                   'task_target':widgets.Textarea(attrs={'class':'form-control','placeholder':'扫描目标,ip/url'}),
                   'task_targetinfo':widgets.Textarea(attrs={'class':'form-control','placeholder':'本次任务说明，如漏洞复查，周期检查、版本更新、上线准备等'}),
                   }