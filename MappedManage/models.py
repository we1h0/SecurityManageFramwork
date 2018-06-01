#coding:utf-8
from django.db import models
from AssetManage.models import Asset,Port_Info
from django.contrib.auth.models import User
# Create your models here.





class Mapped(models.Model):
    LANip = models.ForeignKey(Asset,related_name='LANip_for_mapped',on_delete=models.CASCADE,verbose_name='内网IP')
    LANPort = models.ForeignKey(Port_Info,related_name='LANport_for_mapped',on_delete=models.CASCADE,verbose_name='内网端口')
    
    WANip = models.ForeignKey(Asset,related_name='WANip_for_mapped',on_delete=models.CASCADE,verbose_name='外网IP')
    WANPort = models.ForeignKey(Port_Info,related_name='WANport_for_mapped',on_delete=models.CASCADE,verbose_name='外网端口')
    
    Domain = models.CharField('域名',max_length=50,blank=True,null=True)
    
    mapped_status = models.BooleanField('是否启用',default=True)
    start_time = models.DateField("开启时间",null=True)
    end_time = models.DateField("关闭时间",null=True)
    
    request_email = models.EmailField('申请人邮箱',null=True,blank=True)
    action_email = models.EmailField('操作人邮箱',null=True,blank=True)
    Mapped_description = models.TextField('映射备注',null=True,blank=True)
    
    request_order = models.CharField('申请单号',max_length=50,null=True,blank=True)
    request_user = models.CharField('申请人',max_length=50,null=True,blank=True)
    request_user_num = models.CharField('员工编号',max_length=50,null=True,blank=True)
    request_user_department = models.CharField('申请部门',max_length=50,null=True,blank=True)
    telephone = models.CharField('联系电话',max_length=50,null=True,blank=True)
    
    mapped_updatetime = models.DateTimeField('更新时间',auto_now=True)
    
    Mapped_user = models.ManyToManyField(User,related_name='mapped_to_user',blank=True)
    
    def __str__(self):
        return self.asset_key