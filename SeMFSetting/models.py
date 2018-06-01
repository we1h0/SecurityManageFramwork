#coding:utf-8
#coding:utf-8
from django.db import models
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
                ('APP',(
                        ('MobSF','MobSF'),
                        )
                 ),
                )
SCANNER_STATUS = (
                ('启用','启用'),
                ('禁用','禁用'),
                )


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
    policies_name = models.CharField('策略名称',max_length=50)
    scanner = models.ForeignKey(Scanner,verbose_name='节点关联',related_name='police_for_scanner',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.policies_name
    
    
    