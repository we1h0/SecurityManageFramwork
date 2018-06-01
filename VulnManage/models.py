#coding:utf-8
from django.db import models
from AssetManage.models import Asset
from SeMFSetting.models import SCANNER_TYPE

# Create your models here.
VULN_LEAVE=(
            ('0','信息'),
            ('1','低危'),
            ('2','中危'),
            ('3','高危'),
            ('4','紧急'),
            )
VULN_STATUS=(
             ('0','已忽略'),
             ('1','已修复'),
             ('2','待修复'),
             ('3','漏洞重现'),
             ('4','复查中'),
             )


class Advance_vulns(models.Model):
    type = models.CharField('漏洞类型',max_length=50,choices=SCANNER_TYPE)
    vuln_name=models.CharField('漏洞名称',max_length=255)
    leave = models.CharField('危险等级',max_length=10,choices=VULN_LEAVE)
    fix = models.TextField('修复方案',null=True)
    create_data = models.DateTimeField('发现时间',auto_now_add=True)
    update_data = models.DateTimeField('修复时间',auto_now=True)
    def __str__(self):
        return self.vuln_name


class Cnvdfiles(models.Model):
    title = models.CharField('文件标题',max_length=50)
    file = models.FileField('CNVD文件',upload_to ='cnvd/')
    update_data = models.DateField("更新日期",auto_now=True)
    
    def __str__(self):
        return self.title

# Create your models here.
class Vulnerability(models.Model):
    cve_id = models.CharField('漏洞编号',max_length=30)
    cnvd_id = models.CharField('cnvd编号',max_length=30,null=True)
    cve_name=models.CharField('漏洞名称',max_length=255)
    leave = models.CharField('危险等级',max_length=10)
    introduce = models.TextField('漏洞简介')
    scopen = models.TextField('影响范围')
    fix = models.TextField('修复方案')
    fix_step = models.URLField('修复指南',null=True,blank=True)
    update_data = models.DateTimeField("更新日期",auto_now=True)
    def __str__(self):
        return self.cve_id
    
class Vulnerability_scan(models.Model):
    vuln_id = models.CharField('漏洞编号',max_length=30)
    vuln_name=models.CharField('漏洞名称',max_length=255)
    cve_name=models.CharField('cve编号',max_length=50,null=True,blank=True)
    vuln_type = models.CharField('漏洞属性',max_length=60)
    leave = models.CharField('危险等级',max_length=10,choices=VULN_LEAVE)
    introduce = models.TextField('漏洞简介',null=True)
    vuln_info = models.TextField('漏洞信息',null=True)
    scopen = models.TextField('影响范围')
    fix = models.TextField('修复方案',null=True)
    fix_action = models.TextField('处理记录',null=True)
    fix_status = models.CharField('修复状态',max_length=30,choices=VULN_STATUS)
    create_data = models.DateTimeField('发现时间',auto_now_add=True)
    update_data = models.DateTimeField('修复时间',auto_now=True)
    
    vuln_asset = models.ForeignKey(Asset,related_name='vuln_for_asset',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vuln_id