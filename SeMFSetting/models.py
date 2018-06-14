#coding:utf-8
#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from AssetManage.models import AssetType

# Create your models here.
SCANNER_TYPE = (
                ('WEB',(
                        ('AWVS','AWVS'),
                        )
                 ),
                ('System',(
                           ('Nessus','Nessus'),
                           )
                 ),
                )
SCANNER_STATUS = (
                ('启用','启用'),
                ('禁用','禁用'),
                )

FILE_TYPE = (
    ('网络设备','网络设备'),
    ('业务系统','业务系统'),
    ('漏洞列表','漏洞列表'),
    )

class files(models.Model):
    name = models.CharField('名称',max_length=50,null=True)
    file_type = models.CharField('类型',max_length=50,choices=FILE_TYPE)
    file = models.FileField('批量文件',upload_to ='files/')
    update_data = models.DateField("更新日期",auto_now=True)
    
    action_user = models.ForeignKey(User,related_name='asset_files_user',on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name




class Scanner(models.Model):
    scanner_name = models.CharField('节点名称',max_length=50)
    scanner_type = models.CharField('节点类型',max_length=50,choices=SCANNER_TYPE)
    scanner_url = models.URLField('节点地址',max_length=50)
    scanner_status = models.CharField('节点状态',max_length=50,default='禁用',choices=SCANNER_STATUS)
    scanner_apikey = models.CharField('API_KEY',max_length=100)
    scanner_apisec = models.CharField('API_SEC',max_length=100,blank=True)
    scanner_des = models.TextField('节点描述')
    scanner_addtime = models.DateField('开始时间',auto_now_add=True)    #任务开始时间
    scanner_updatetime = models.DateField('结束时间',auto_now=True)      #任务结束时间
    
    assetType = models.ManyToManyField(AssetType,verbose_name='扫描范围',related_name='scanner_assettype',limit_choices_to={'parent__isnull':False})
    
    def __str__(self):
        return self.scanner_name
    
    
class ScannerPolicies(models.Model):
    policies_name = models.CharField('策略名称',max_length=50,help_text='扫描策略为扫描器策略名称')
    policies_key = models.CharField('策略编号',max_length=50,null=True,blank=True,help_text='AWVS扫描器需填写，全扫描编号为11111111-1111-1111-1111-111111111111')
    scanner = models.ForeignKey(Scanner,verbose_name='节点关联',related_name='police_for_scanner',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.policies_name
    
    
    