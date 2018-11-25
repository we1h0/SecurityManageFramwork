#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from RBAC.models import Area,REQUEST_STATUS
# Create your models here.

ASSET_REQUEST_ACTION = (
                        ('工作交接','工作交接'),
                        ('资产认领','资产认领'),
                        )

ASSET_REQUEST_STATUS=(
    ('0','审批中'),
    ('1','审批通过'),
    ('2','审批拒绝'),
    )




class Handover(models.Model):
    dst_email = models.EmailField('目标账号')
    status = models.CharField('申请状态',max_length = 30,choices=ASSET_REQUEST_STATUS,default='0')
    reason = models.TextField('转让说明')
    action_reason = models.TextField('审批说明')
    request_starttime = models.DateField('添加时间',auto_now_add=True)
    request_updatetime = models.DateField('更新时间',auto_now=True)
    
    request_user = models.EmailField('申请账号')
    
    action_user = models.ForeignKey(User,related_name='handover_action_user',on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.id




class AssetType(models.Model):
    name = models.CharField('资产分类',max_length = 30)
    description = models.TextField('资产简介')
    parent = models.ForeignKey('self',verbose_name='父菜单',related_name='assettype_type',null=True,blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        #显示层级菜单
        return self.name
    
class AssetTypeInfo(models.Model):
    key = models.CharField('属性标识',max_length = 30,unique=True,null=True)
    name = models.CharField('资产属性',max_length = 30)
    type_connect = models.ManyToManyField(AssetType,verbose_name='属性关联',related_name='typeinfo_assettype',blank=True)
    
    def __str__(self):
        return self.name




ASSET_STATUS=(
                ('0','使用中'),
                ('1','闲置中'),
                ('2','已销毁'),
                )
    
class Asset(models.Model):
    asset_id = models.CharField('系统编号',max_length=50,unique=True,null=True)
    asset_out_id = models.CharField('资产编号',max_length=50,null=True,blank=True)
    asset_name = models.CharField('资产名称',max_length = 100)
    asset_key = models.CharField('唯一标记',max_length=50,unique=True)
    asset_description = models.TextField('资产介绍',null=True)
    asset_score = models.IntegerField('重要性估值',default = '0')
    asset_status = models.CharField('资产状态',max_length = 50,choices=ASSET_STATUS,default='0')
    asset_check = models.BooleanField('是否检查',default=False)
    asset_inuse = models.BooleanField('是否认领',default=False)
    asset_starttime = models.DateTimeField('添加时间',auto_now_add=True)
    asset_updatetime = models.DateTimeField('更新时间',auto_now=True)
    
    user_email=models.EmailField('联系人邮箱',null=True,blank=True)
    
    asset_area = models.ForeignKey(Area,related_name='area_for_asset',verbose_name='所属区域',on_delete=models.CASCADE,null=True,blank=True)
    asset_type = models.ForeignKey(AssetType,related_name='type_for_asset',verbose_name='资产类型',on_delete=models.CASCADE,null=True,limit_choices_to={'parent__isnull':False})
    asset_user = models.ManyToManyField(User,related_name='asset_to_user',blank=True)
    
    asset_connect = models.ManyToManyField('self',verbose_name='资产关联',related_name='asset_asset',blank=True)
    
    def __str__(self):
        return self.asset_key
    
    
    
class AssetRequest(models.Model):
    asset_key = models.CharField('申请对象',max_length = 30)
    asset_request_status = models.CharField('状态',max_length = 30,choices=REQUEST_STATUS,default='0')
    request_action = models.CharField('操作类型',max_length = 30,choices=ASSET_REQUEST_ACTION)
    request_reason = models.TextField('申请理由',null=True)
    request_note = models.TextField('审批备注',null=True)
    request_starttime = models.DateTimeField('添加时间',auto_now_add=True)
    request_updatetime = models.DateTimeField('更新时间',auto_now=True)
    
    request_user = models.ForeignKey(User,related_name='assetrequest_for_user',on_delete=models.CASCADE)
    asset_type = models.ForeignKey(AssetType,related_name='type_for_assetrequest',verbose_name='资产类型',on_delete=models.CASCADE,null=True,limit_choices_to={'parent__isnull':False})
    action_user = models.ForeignKey(User,related_name='assetrequestaction_for_user',on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.asset_key



WEB_LANGUAGE=(
    ('C/C++','C/C++'),
    ('C#','C#'),
    ('Ruby','Ruby'),
    ('JAVA','JAVA'),
    ('ASP.NET','ASP.NET'),
    ('JSP','JSP'),
    ('PHP','PHP'),
    ('Perl','Perl'),
    ('Python','Python'),
    ('VB.NET','VB.NET'),
    ('Other','Other'),
    )

WEB_STATUS=(
            ('0','测试系统'),
            ('1','演示系统'),
            ('3','内部使用'),
            ('4','商用系统'),
            )


class OS_Info(models.Model):
    hostname = models.CharField(max_length=50, verbose_name="主机名")
    os = models.CharField("操作系统", max_length=100, blank=True)
    vendor = models.CharField("设备厂商", max_length=50, blank=True)
    cpu_model = models.CharField("CPU型号", max_length=100, blank=True)
    cpu_num = models.CharField("CPU数量", max_length=100, blank=True)
    memory = models.CharField("内存大小", max_length=30, blank=True)
    disk = models.CharField("硬盘大小", max_length=255, blank=True)
    monitor= models.CharField("监控关联", max_length=30, blank=True)
    sn = models.CharField("SN号 码", max_length=60, blank=True)
    cabinet = models.CharField("机柜信息", max_length=50, blank=True)
    
    up_time = models.DateField("上架时间",null=True)
    guarante_time = models.DateField("保修时间",null=True)
    down_time = models.DateField("停用时间",null=True)
    updatetime = models.DateField('更新时间',auto_now=True)
    
    asset = models.OneToOneField(Asset,related_name='os_for_asset',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.asset.asset_key




class Internet_Info(models.Model):
    middleware = models.CharField('中间件',max_length=50,blank=True,null=True)
    middleware_version = models.CharField('版本',max_length=50,blank=True,null=True)
    is_out = models.BooleanField('是否发布',default=False)
    out_key = models.CharField('域名',max_length=50,blank=True,null=True)
    web_status = models.CharField('状态说明',max_length = 50,choices=WEB_STATUS,default='测试系统')
    language = models.CharField('开发语言',max_length = 50,choices=WEB_LANGUAGE,null=True)
    language_version = models.CharField('语言版本',max_length = 50,blank=True,null=True)
    web_framwork = models.CharField('开发框架',max_length = 50,blank=True,null=True)
    web_framwork_version = models.CharField('开发框架版本',max_length = 50,blank=True,null=True)
    updatetime = models.DateField('更新时间',auto_now=True)
    
    asset = models.OneToOneField(Asset,related_name='internet_for_asset',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.asset.asset_key



class Port_Info(models.Model):
    port = models.CharField('开放端口',max_length=50)
    name = models.CharField('服务名称',max_length=50,null=True)
    product = models.CharField('产品信息',max_length=100,null=True)
    version = models.CharField('应用版本',max_length=50,null=True)
    port_info = models.TextField('端口介绍',null=True)
    updatetime = models.DateField('更新时间',auto_now=True)
    
    asset = models.ForeignKey(Asset,related_name='port_for_asset',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.port

class Plugin_Info(models.Model):
    name = models.CharField('组件名称',max_length=50)
    version = models.CharField('应用版本',max_length=50,null=True)
    plugin_info = models.TextField('组件简介',null=True)
    starttime = models.DateTimeField('添加时间',auto_now_add=True)
    updatetime = models.DateField('更新时间',auto_now=True)
    
    asset = models.ForeignKey(Asset,related_name='plugin_for_asset',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class File(models.Model):
    name = models.CharField('附件名称',max_length=50)
    file = models.FileField('附件内容',upload_to ='assetfiles/%Y/%m/%d/')
    file_info = models.TextField('附件说明',null=True)
    updatetime = models.DateField('更新时间',auto_now=True)
    
    asset = models.ForeignKey(Asset,related_name='file_for_asset',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
class AssetUser(models.Model):
    dst_user_email = models.EmailField('目标账号')
    reason = models.TextField('指定说明')
    asset_list = models.TextField('资产列表')
    request_updatetime = models.DateField('更新时间',auto_now=True)
    
    action_user = models.ForeignKey(User,related_name='assetuser_action_user',on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.dst_user_email   
