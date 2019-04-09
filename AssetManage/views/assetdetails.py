#coding:utf-8
'''
Created on 2018年5月17日

@author: yuguanc
'''

from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .. import models
from django.http import JsonResponse
from SeMFSetting.views import paging
from VulnManage.views.views import VULN_LEAVE,VULN_STATUS
from django.db.models import Count
from django.utils.html import escape


ASSET_STATUS={
    '0':'使用中',
    '1':'闲置中',
    '2':'已销毁',
    }

@login_required
def assetdetailsview(request,asset_id):
    user = request.user
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
        
    vuln_all = asset.vuln_for_asset.all()
    vuln_count = vuln_all.count()
    vuln_ign = vuln_all.filter(fix_status = 0).count()
    vuln_fixed = vuln_all.filter(fix_status = 1).count()
    vuln_fix = vuln_all.exclude(fix_status__in=[0,1]).count()
        
    vuln_status = {
            'vuln_count':vuln_count,
            'vuln_ign':vuln_ign,
            'vuln_fixed':vuln_fixed,
            'vuln_fix':vuln_fix
            }
    
    assettypeinfo = asset.asset_type.parent.typeinfo_assettype.all() | asset.asset_type.typeinfo_assettype.all()
    
    info = []
    
    for typeinfo in assettypeinfo:
        info.append(typeinfo.key)
    
    if 'os' in info:
        try:
            os_info = asset.os_for_asset
        except:
            models.OS_Info.objects.get_or_create(asset=asset)
            os_info = asset.os_for_asset
    else:
        os_info = ''
            
    if 'internet' in info:
        try:
            internet_info = asset.internet_for_asset
        except:
            internet_info = models.Internet_Info.objects.get_or_create(asset=asset)
            internet_info=internet_info[0]
    else:
        internet_info=''
    
    return render(request,'AssetManage/assetdetails.html',{'asset':asset,'info':info,'os_info':os_info,'internet_info':internet_info,'vuln_status':vuln_status})


@login_required
def asset_ports(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    port_list = asset.port_for_asset.all().order_by('-updatetime')
    total = port_list.count()
    #port_list = paging(port_list,rows,page)
    data = []
    for port in port_list:
        dic={}
        dic['id']=escape(port.id)
        dic['port']=escape(port.port)
        dic['product']=escape(port.product)
        dic['version']=escape(port.version)
        dic['port_info']=escape(port.port_info)
        dic['updatetime']=escape(port.updatetime)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)


@login_required
def asset_vuln(request,asset_id):
    user  = request.user
    resultdict={}
    
    page = request.GET.get('page')
    rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    vuln_list = asset.vuln_for_asset.all().order_by('-fix_status','-leave')
    total = vuln_list.count()
    vuln_list = paging(vuln_list,rows,page)
    data = []
    for vuln in vuln_list:
        dic={}
        dic['vuln_id'] =escape(vuln.vuln_id)
        dic['cve_name'] =escape(vuln.cve_name)
        dic['vuln_name'] =escape(vuln.vuln_name)
        dic['vuln_type'] =escape(vuln.vuln_type)
        dic['leave'] =escape(VULN_LEAVE[vuln.leave])
        dic['fix_status'] =escape(VULN_STATUS[vuln.fix_status])
        dic['update_data'] =escape(vuln.update_data)
        dic['asset'] =escape(vuln.vuln_asset.asset_key)
        dic['asset_id'] =escape(vuln.vuln_asset.asset_id)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)

        
        
@login_required
def asset_plugin(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    plugin_list = asset.plugin_for_asset.all().order_by('-updatetime')
    total = plugin_list.count()
    #plugin_list = paging(plugin_list,rows,page)
    data = []
    for plugin in plugin_list:
        dic={}
        dic['id']=escape(plugin.id)
        dic['name']=escape(plugin.name)
        dic['version']=escape(plugin.version)
        dic['plugin_info']=escape(plugin.plugin_info)
        dic['updatetime']=escape(plugin.updatetime)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)        


@login_required
def asset_file(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    file_list = asset.file_for_asset.all().order_by('-updatetime')
    total = file_list.count()
    #file_list = paging(file_list,rows,page)
    data = []
    for file in file_list:
        dic={}
        dic['id']=escape(file.id)
        dic['name']=escape(file.name)
        dic['file']=escape( '/uploads/'+str(file.file))
        dic['file_info']=escape(file.file_info)
        dic['updatetime']=escape(file.updatetime)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict) 


@login_required
def asset_asset(request,asset_id):
    user  = request.user
    resultdict={}
    
    #page = request.GET.get('page')
    #rows = request.GET.get('limit')
    
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    assetconnect_list = asset.asset_connect.all().order_by('-asset_updatetime')
    total = assetconnect_list.count()
    #assetconnect_list = paging(assetconnect_list,rows,page)
    data = []
    for assetconnect in assetconnect_list:
        dic={}
        dic['asset_id'] =escape( assetconnect.asset_id)
        dic['asset_name'] =escape( assetconnect.asset_name)
        dic['asset_key'] =escape( assetconnect.asset_key)
        dic['asset_status'] =escape( ASSET_STATUS[assetconnect.asset_status])
        if assetconnect.asset_inuse:
            dic['asset_inuse'] =escape( '已认领')
        else:
            dic['asset_inuse'] =escape( '待认领')
        if assetconnect.asset_type:
            dic['asset_type'] =escape( assetconnect.asset_type.name)
        else:
            dic['asset_type'] =escape( '未分类')
        dic['user_email'] =escape( assetconnect.user_email)
        dic['asset_score'] =escape( assetconnect.asset_score)
        dic['asset_updatetime'] =escape( assetconnect.asset_updatetime)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="端口列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)     



