#! /usr/bin/python3
# -*- coding:UTF-8 -*-

import django,os

def initmenu():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from RBAC import models
    menu_list = [
                 {'title':'资产管理','icon':"&#xe653;"},
                 {'title':'网络映射','icon':"&#xe674;"},
                 {'title':'漏洞管理','icon':"&#xe663;"},
                 {'title':'任务管理','icon':"&#xe628;"},
                 {'title':'报表中心','icon':"&#xe629;"},
                 {'title':'知识共享','icon':"&#xe705;"},
                 {'title':'用户管理','icon':"&#xe770;"},
                 ]
    for item in menu_list:
        models.Menu.objects.get_or_create(
                                   title = item['title'],
                                   icon = item['icon']
                                   )
        
    submain_list = [
                    {'title':'资产列表','icon':"&#xe60a;",'parent_title':'资产管理'},
                    {'title':'资产审批','icon':"&#xe60b;",'parent_title':'资产管理'},
                    {'title':'交接审批','icon':"&#xe607;",'parent_title':'资产管理'},
                    
                    {'title':'映射列表','icon':"&#xe60a;",'parent_title':'网络映射'},
                    
                    {'title':'漏洞列表','icon':"&#xe756;",'parent_title':'漏洞管理'},
                    {'title':'漏洞库','icon':"&#xe656;",'parent_title':'漏洞管理'},
                    
                    {'title':'任务列表','icon':"&#xe60a;",'parent_title':'任务管理'},
                    {'title':'任务审批','icon':"&#xe60b;",'parent_title':'任务管理'},
                    
                    {'title':'基础报表','icon':"&#xe629;",'parent_title':'报表中心'},
                    
                    {'title':'知识库','icon':"&#xe705;",'parent_title':'知识共享'},
                    
                    {'title':'用户列表','icon':"&#xe60a;",'parent_title':'用户管理'},
                    {'title':'用户审批','icon':"&#xe60b;",'parent_title':'用户管理'},
                    
                    ]
    
    for item in submain_list:
        models.Menu.objects.get_or_create(
                                   title = item['title'],
                                   icon = item['icon'],
                                   parent = models.Menu.objects.filter(title = item['parent_title']).first(),
                                   )
        
    permission_list = [
                       {'title':'资产列表','url':'/asset/user/','is_menu':True,'menu_title':'资产列表'},
                       {'title':'资产审批','url':'/asset/request/','is_menu':True,'menu_title':'资产审批'},
                       {'title':'交接审批','url':'/asset/handover/','is_menu':True,'menu_title':'交接审批'},
                       {'title':'资产指定','url':'/asset/manage/','is_menu':False},
                       
                       {'title':'映射列表','url':'/mapped/','is_menu':True,'menu_title':'映射列表'},
                       
                       {'title':'漏洞操作','url':'/vuln/manage/','is_menu':False},
                       {'title':'漏洞列表','url':'/vuln/user/','is_menu':True,'menu_title':'漏洞列表'},
                       {'title':'漏洞库','url':'/vuln/cnvd/','is_menu':True,'menu_title':'漏洞库'},
                       
                       {'title':'任务列表','url':'/task/user/','is_menu':True,'menu_title':'任务列表'},
                       {'title':'任务审批','url':'/task/request/','is_menu':True,'menu_title':'任务审批'},
                       {'title':'扫描同步','url':'/task/manage/','is_menu':False},
                       
                       {'title':'基础报表','url':'/chart/','is_menu':True,'menu_title':'基础报表'},
                       
                       {'title':'知识库','url':'/article/user/','is_menu':True,'menu_title':'知识库'},
                       {'title':'知识库更新','url':'/article/manage/','is_menu':False},
                       
                       {'title':'用户列表','url':'/manage/user/','is_menu':True,'menu_title':'用户列表'},
                       {'title':'用户审批','url':'/manage/userrequest/','is_menu':True,'menu_title':'用户审批'},
                       
                       ]
    for item in permission_list:
        permission_tup = models.Permission.objects.get_or_create(
                                         title=item['title'],
                                         url = item['url']
                                         )
        permission = permission_tup[0]
        if item['is_menu']:
            permission.menu = models.Menu.objects.filter(title = item['menu_title']).first()
            permission.save()



        
def initassettype():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from AssetManage.models import AssetType
    assettype_list = [
                        {'name':'网络设备','description':'主要为网络设备，比如，服务器、防火墙、摄像头等','parent':''},
                        {'name':'应用资产','description':'主要为网站、应用系统等','parent':''},
                        {'name':'APP资产','description':'主要为网站、应用系统等','parent':''},
                        {'name':'特殊资产','description':'主要网段等','parent':''},
                        
                        {'name':'服务器','description':'资产发现默认','parent':'网络设备'},
                        {'name':'实体机','description':'物理服务器','parent':'网络设备'},
                        {'name':'虚拟机','description':'VM虚拟机','parent':'网络设备'},
                        {'name':'路由器','description':'路由器设备','parent':'网络设备'},
                        {'name':'交换机','description':'交换机设备','parent':'网络设备'},
                        {'name':'安全设备','description':'安全设备','parent':'网络设备'},
                        {'name':'打印机','description':'打印机设备','parent':'网络设备'},
                        {'name':'摄像头','description':'摄像头设备','parent':'网络设备'},
                        {'name':'其他设备','description':'其他设备','parent':'网络设备'},
                        
                        {'name':'WEB应用','description':'主要为web网站等','parent':'应用资产'},
                        
                        {'name':'移动APP','description':'主要为apk、ipa、appx等','parent':'APP资产'},
                        
                        {'name':'IP地址段','description':'主要网段等','parent':'特殊资产'},
                        {'name':'公网IP','description':'外网ip','parent':'特殊资产'},
                        ]
    for item in assettype_list:
        if item['parent'] == '':
            parent_assettype=''
        else:
            parent_assettype = AssetType.objects.filter(name=item['parent']).first()
        if parent_assettype:
            AssetType.objects.get_or_create(
                name = item['name'],
                description = item['description'],
                parent = parent_assettype,
                )
        else:
            AssetType.objects.get_or_create(
                name = item['name'],
                description = item['description'],
                )
    print('initassettype ok')


def initassettypeinfo():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from AssetManage.models import AssetType,AssetTypeInfo
    role_list =[
        {'name':'设备信息','key':'os','type_connect':'网络设备'},
        
        {'name':'端口信息','key':'port','type_connect':'网络设备'},
        {'name':'端口信息','key':'port','type_connect':'公网IP'},
        
        {'name':'安全隐患','key':'vuln','type_connect':'网络设备'},
        {'name':'安全隐患','key':'vuln','type_connect':'应用资产'},
        {'name':'安全隐患','key':'vuln','type_connect':'APP资产'},
        
        {'name':'Web信息','key':'internet','type_connect':'应用资产'},
        {'name':'Web信息','key':'internet','type_connect':'APP资产'},
        
        {'name':'插件信息','key':'plugin','type_connect':'应用资产'},
        {'name':'插件信息','key':'plugin','type_connect':'APP资产'},
        
        {'name':'附加文件','key':'file','type_connect':'网络设备'},
        {'name':'附加文件','key':'file','type_connect':'应用资产'},
        {'name':'附加文件','key':'file','type_connect':'APP资产'},
        
        ]
    for item in role_list:
        asset_typeinfo = AssetTypeInfo.objects.get_or_create(
            key = item['key'],
            name = item['name']
            )
        asset_typeinfo = asset_typeinfo[0]
        asset_typeinfo.type_connect.add(AssetType.objects.filter(name=item['type_connect']).first())
        asset_typeinfo.save()
    print('initassettypeinfo ok')
     

def initrole():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from RBAC.models import Role,Permission
    permissions_list=[
        {'title':'安全管理员','permissions':'资产列表'},
        {'title':'安全管理员','permissions':'资产审批'},
        {'title':'安全管理员','permissions':'交接审批'},
        {'title':'安全管理员','permissions':'资产指定'},
        {'title':'安全管理员','permissions':'映射列表'},
        {'title':'安全管理员','permissions':'漏洞操作'},
        {'title':'安全管理员','permissions':'漏洞列表'},
        {'title':'安全管理员','permissions':'漏洞库'},
        {'title':'安全管理员','permissions':'任务列表'},
        {'title':'安全管理员','permissions':'任务审批'},
        {'title':'安全管理员','permissions':'扫描同步'},
        {'title':'安全管理员','permissions':'基础报表'},
        {'title':'安全管理员','permissions':'知识库'},
        {'title':'安全管理员','permissions':'知识库更新'},
        {'title':'安全管理员','permissions':'用户列表'},
        {'title':'安全管理员','permissions':'用户审批'},
        
        
        {'title':'运维管理员','permissions':'资产列表'},
        {'title':'运维管理员','permissions':'漏洞列表'},
        {'title':'运维管理员','permissions':'漏洞库'},
        {'title':'运维管理员','permissions':'任务列表'},
        {'title':'运维管理员','permissions':'基础报表'},
        {'title':'运维管理员','permissions':'知识库'},
        
        {'title':'网络管理员','permissions':'资产列表'},
        {'title':'网络管理员','permissions':'映射列表'},
        {'title':'网络管理员','permissions':'漏洞列表'},
        {'title':'网络管理员','permissions':'漏洞库'},
        {'title':'网络管理员','permissions':'任务列表'},
        {'title':'网络管理员','permissions':'基础报表'},
        {'title':'网络管理员','permissions':'知识库'},
        
        {'title':'业务负责人','permissions':'资产列表'},
        {'title':'业务负责人','permissions':'漏洞列表'},
        {'title':'业务负责人','permissions':'漏洞库'},
        {'title':'业务负责人','permissions':'任务列表'},
        {'title':'业务负责人','permissions':'基础报表'},
        {'title':'业务负责人','permissions':'知识库'},
        ]
    for item in permissions_list:
        role_list = Role.objects.get_or_create(title=item['title'])
        role_list[0].permissions.add(Permission.objects.filter(title = item['permissions']).first())
        role_list[0].save()
        
    print('initrole ok')

def initarea():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from RBAC.models import Area
    area_list =[
        {'name':'华北'},
        {'name':'华南'},
        {'name':'华东'},
        {'name':'华中'},
        ]
    for item in area_list:
        Area.objects.get_or_create(name=item['name'])
    print('initrole ok')

    
def initsuperuser():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from RBAC.models import Role
    from django.contrib.auth.models import User
    user_manage_list = User.objects.filter(is_superuser=True)
    role = Role.objects.filter(title='安全管理员').first()
    for user in user_manage_list:
        user.profile.roles.add(role)
        user.save()
    print('initsuperuser ok')
    
def initarticle():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from ArticleManage.models import ArticleType
    articletype_list = [
                        {'article_type_name':'通告','article_type_body':'通告类型','parent':''},
                        {'article_type_name':'科普','article_type_body':'通告类型','parent':''},
                        {'article_type_name':'系统通告','article_type_body':'系统通告类','parent':'通告'},
                        {'article_type_name':'安全预警','article_type_body':'漏洞预警类','parent':'通告'},
                        {'article_type_name':'安全开发','article_type_body':'该类包含安全开发类知识','parent':'科普'},
                        {'article_type_name':'安全培训','article_type_body':'该类包含安全培训类知识','parent':'科普'},
                        {'article_type_name':'漏洞修复方案','article_type_body':'该类包含安全漏洞修复方案/修复指南','parent':'科普'},
                        ]
    for item in articletype_list:
        articletype=ArticleType.objects.get_or_create(
                                          article_type_name = item['article_type_name'],
                                          article_type_body = item['article_type_body'],
                                          )
        if item['parent']:
            parent = ArticleType.objects.filter(article_type_name=item['parent']).first()
            if parent:
                articletype[0].parent=parent
                articletype[0].save()
        
    print('initarticle ok')

        
if __name__ == "__main__":
    initmenu()
    initassettype()
    initassettypeinfo()
    initrole()
    initarea()
    initsuperuser()
    initarticle()
    