#coding:utf-8

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from AssetManage.models import Asset
from SeMFSetting.models import Scanner,ScannerPolicies
# Create your models here.
TASK_TYPE = (
             ('安全扫描','安全扫描'),
             ('扫描同步','扫描同步'),
             )

TASK_STATUS=(
             ('0','审批中'),
             ('1','待执行'),
             ('2','执行中'),
             ('3','已暂停'),
             ('4','已完成'),
             ('5','已结束'),
             )

REQUEST_STATUS=(
                ('0','审批中'),
                ('1','审批通过'),
                ('2','审批拒绝'),
                )


class Task(models.Model):
    task_id = models.CharField('任务编号',max_length=50)      #任务id
    scan_id = models.CharField('扫描编号',max_length=100,null=True)
    task_name = models.CharField('任务名称',max_length=30)     #任务名称
    task_type = models.CharField('任务类型',max_length=25, choices=TASK_TYPE)     #任务类型
    task_target = models.TextField('任务目标',null = True)   #任务目标
    task_targetinfo = models.TextField('任务描述')            #目标描述
    task_status = models.CharField('任务状态',max_length=20,choices=TASK_STATUS)    #任务状态     四个状态，创建，审批中，执行中，结束 ״
    task_plan_time = models.DateTimeField('计划执行时间',null=True,blank=True)     #计划执行时间
    task_plan_end_time = models.DateTimeField('计划结束时间',null=True)     #计划执行时间
    request_status = models.CharField('请求状态',max_length =50,choices=REQUEST_STATUS)
    request_note = models.TextField('审批备注',null=True)       #安全人员审批扫描时的备注
    task_starttime = models.DateTimeField('开始时间',auto_now_add=True)    #任务开始时间
    task_endtime = models.DateTimeField('更新时间',auto_now=True)      #任务结束时间
    
    task_asset = models.ManyToManyField(Asset,related_name='asset_to_task',verbose_name='资产关联')
    
    task_scanner = models.ForeignKey(Scanner,related_name='scanner_to_task',on_delete=models.CASCADE,verbose_name='扫描器')
    scanner_police = models.ForeignKey(ScannerPolicies,related_name='police_to_scanner',null=True,on_delete=models.CASCADE,verbose_name='扫描策略')
    
    task_user = models.ForeignKey(User,related_name='task_for_user',on_delete=models.CASCADE,verbose_name='任务用户')
    action_user = models.ForeignKey(User,related_name='taskrequestaction_for_user',on_delete=models.CASCADE,null=True,blank=True)
                                                                     
    def __str__(self):
        return self.task_id