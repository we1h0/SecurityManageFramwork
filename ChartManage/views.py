#coding:utf-8

from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
from AssetManage.models import Asset
from VulnManage.models import Vulnerability_scan
from VulnManage.views.views import VULN_LEAVE,VULN_STATUS
from django.db.models import Count
from django.http import JsonResponse
from .Functions.publicfunction import datelist
from django.utils import timezone
from django.db import connection
from datetime import timedelta

@login_required
def chartview(request):
    is_asset = False
    asset = Asset.objects.all()
    if asset:
        is_asset = True
    
    is_vuln = False
    vuln = Vulnerability_scan.objects.all()
    if vuln:
        is_vuln = True
    
    is_danger = False
    vuln = Vulnerability_scan.objects.filter(leave__gte=3)
    if vuln:
        is_danger = True
        
    
    return render(request,'ChartManage/chartview.html',{'is_asset':is_asset,'is_vuln':is_vuln,'is_danger':is_danger})



@login_required
def getassettype(request):
    user = request.user
    result={
        'categories':[],
        'data':[],
        }
    if user.is_superuser:
        asset_type = Asset.objects.all().values('asset_type__name').annotate(number=Count('id'))
    else:
        asset_type = Asset.objects.filter(asset_user = user).values('asset_type__name').annotate(number=Count('id'))
    
    if asset_type:
        for item in asset_type:
            result['categories'].append(item['asset_type__name'])
            result['data'].append({'name':item['asset_type__name'],'value':item['number']})
    return JsonResponse(result)


@login_required
def getvulnname(request):
    user = request.user
    result={
        'categories':[],
        'data':[],
        }
    if user.is_superuser:
        vuln_name = Vulnerability_scan.objects.exclude(fix_status__in=[0,1]).filter(leave__gte=3).values('vuln_name').annotate(number=Count('id'))
    else:
        vuln_name = Vulnerability_scan.objects.filter(vuln_asset__asset_user = user,leave__gte=3).exclude(fix_status__in=[0,1]).values('vuln_name').annotate(number=Count('id'))
    if vuln_name:
        for item in vuln_name:
            result['categories'].append(item['vuln_name'])
            result['data'].append(item['number'])
    return JsonResponse(result)
    
    
@login_required
def getvulnleave(request):
    user = request.user
    result={
        'categories':[],
        'data':[],
        }
    if user.is_superuser:
        vuln_leave = Vulnerability_scan.objects.exclude(fix_status__in=[0,1]).values('leave').annotate(number=Count('id'))
    else:
        vuln_leave = Vulnerability_scan.objects.filter(vuln_asset__asset_user = user).exclude(fix_status__in=[0,1]).values('leave').annotate(number=Count('id'))
    
    if vuln_leave:
        for item in vuln_leave:
            result['categories'].append(VULN_LEAVE[item['leave']])
            result['data'].append({'name':VULN_LEAVE[item['leave']],'value':item['number']})
    return JsonResponse(result)


@login_required
def getvulnstatus(request):
    user = request.user
    result={
        'categories':[],
        'data':[],
        }
    if user.is_superuser:
        vuln_status = Vulnerability_scan.objects.all().values('fix_status').annotate(number=Count('id'))
    else:
        vuln_status = Vulnerability_scan.objects.filter(vuln_asset__asset_user = user).values('fix_status').annotate(number=Count('id'))
    
    if vuln_status:
        for item in vuln_status:
            result['categories'].append(VULN_STATUS[item['fix_status']])
            result['data'].append({'name':VULN_STATUS[item['fix_status']],'value':item['number']})
    return JsonResponse(result)


def getdatemonth(request):
    user = request.user
    argu = 'day'
    
    result={
        'date':[],
        'asset_date':[],
        'vuln_create':[],
        'vuln_fixed':[],
        }
    
    
    date = datelist(30)
    
    result['date'] = date
    
    current_date = timezone.now()
    select = {argu:connection.ops.date_trunc_sql(argu,'asset_starttime')}
    
    #统计近一个月内每天资产新增数量
    if user.is_superuser:
        asset_date = Asset.objects.filter(asset_starttime__range=(current_date - timedelta(days=30), current_date)).extra(select=select).values(argu).annotate(number=Count('id'))
    else:
        asset_date = Asset.objects.filter(asset_user = user).filter(asset_starttime__range=(current_date - timedelta(days=30), current_date)).extra(select=select).values(argu).annotate(number=Count('id'))
    res_data = {}
    for item in asset_date:
        res_data[item[argu].strftime('%Y-%m-%d')]=item['number']
        #res_data[item[argu]]=item['number']
    res_date_keys = res_data.keys()
    for item in date:
        if item in res_date_keys:
            result['asset_date'].append(res_data[item])
        else:
            result['asset_date'].append(0)
    
    #统计一个月内每天新发现的漏洞数量
    select = {argu:connection.ops.date_trunc_sql(argu,'create_data')}
    if user.is_superuser:
        vuln_create_date = Vulnerability_scan.objects.filter(create_data__range=(current_date - timedelta(days=30), current_date)).extra(select=select).values(argu).annotate(number=Count('id'))
    else:
        vuln_create_date = Vulnerability_scan.objects.filter(vuln_asset__asset_user = user).filter(create_data__range=(current_date - timedelta(days=30), current_date)).extra(select=select).values(argu).annotate(number=Count('id'))
    res_data = {}
    for item in vuln_create_date:
        res_data[item[argu].strftime('%Y-%m-%d')]=item['number']
        #res_data[item[argu]]=item['number']
    res_date_keys = res_data.keys()
    for item in date:
        if item in res_date_keys:
            result['vuln_create'].append(res_data[item])
        else:
            result['vuln_create'].append(0)
            
    #统计一个月内每天修复的漏洞数量
    select = {argu:connection.ops.date_trunc_sql(argu,'update_data')}
    if user.is_superuser:
        vuln_fixed_date = Vulnerability_scan.objects.filter(fix_status = '1',update_data__range=(current_date - timedelta(days=30), current_date)).extra(select=select).values(argu).annotate(number=Count('id'))
    else:
        vuln_fixed_date = Vulnerability_scan.objects.filter(vuln_asset__asset_user = user).filter(fix_status = '1',update_data__range=(current_date - timedelta(days=30), current_date)).extra(select=select).values(argu).annotate(number=Count('id'))
    res_data = {}
    for item in vuln_fixed_date:
        res_data[item[argu].strftime('%Y-%m-%d')]=item['number']
        #res_data[item[argu]]=item['number']
    res_date_keys = res_data.keys()
    for item in date:
        if item in res_date_keys:
            result['vuln_fixed'].append(res_data[item])
        else:
            result['vuln_fixed'].append(0)
    
    return JsonResponse(result)

    
    
    