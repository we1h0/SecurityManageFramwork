#coding:utf-8
from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .. import models,forms
from SeMFSetting.views import paging
from django.http import JsonResponse
import time,json
from django.utils.html import escape
# Create your views here.

VULN_LEAVE={
    '0':'信息',
    '1':'低危',
    '2':'中危',
    '3':'高危',
    '4':'紧急'
    }
VULN_STATUS={
    '0':'已忽略',
    '1':'已修复',
    '2':'待修复',
    '3':'漏洞重现',
    '4':'复查中',
    }




@login_required
@csrf_protect
def vuln_change_status(request,vuln_id):
    user = request.user
    error=''
    if user.is_superuser:
        vuln = get_object_or_404(models.Vulnerability_scan,vuln_id=vuln_id)
    else:
        vuln = get_object_or_404(models.Vulnerability_scan,vuln_asset__asset_user=user,vuln_id=vuln_id)
    if vuln:
        if request.method == 'POST':
            form = forms.Vuln_action_form(request.POST,instance=vuln)
            if form.is_valid():
                form.save()
                error = '更改成功'
            else:
                error = '请检查参数'
        else:
            form = forms.Vuln_action_form(instance=vuln)
    else:
        error ='请检查参数'
    return render(request,'formupdate.html',{'form':form,'post_url':'vulnfix','argu':vuln_id,'error':error})




@login_required
@csrf_protect
def vuln_update(request,vuln_id):
    user = request.user
    error=''
    if user.is_superuser:
        vuln = get_object_or_404(models.Vulnerability_scan,vuln_id=vuln_id)
        if vuln:
            if request.method == 'POST':
                form = forms.Vuln_edit_form(request.POST,instance=vuln)
                if form.is_valid():
                    form.save()
                    error = '更改成功'
                else:
                    error = '请检查参数'
            else:
                form = forms.Vuln_edit_form(instance=vuln)
        else:
            error ='请检查参数'
    else:
        error = '权限错误'
    return render(request,'formupdate.html',{'form':form,'post_url':'vulnupdate','argu':vuln_id,'error':error})


@login_required
@csrf_protect
def vulncreate(request,asset_id):
    user = request.user
    error =''
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    if request.method == 'POST':
        form = forms.Vuln_edit_form(request.POST)
        if form.is_valid():
            try:
                num = models.Vulnerability_scan.objects.latest('id').id
            except Exception:
                num = 0
            num =num+1
            vuln_name = form.cleaned_data['vuln_name']
            cve_name = form.cleaned_data['cve_name']
            leave = form.cleaned_data['leave']
            introduce = form.cleaned_data['introduce']
            vuln_info = form.cleaned_data['vuln_info']
            scopen = form.cleaned_data['scopen']
            fix = form.cleaned_data['fix']
            vuln_id = str(asset.asset_type.id) + time.strftime('%Y%m%d',time.localtime(time.time())) + str(num)
            vuln_type = asset.asset_type.name
            res=models.Vulnerability_scan.objects.get_or_create(
                                                                vuln_name=vuln_name,
                                                                 cve_name=cve_name,
                                                                 vuln_type=vuln_type,
                                                                 leave=leave,
                                                                 introduce=introduce,
                                                                 vuln_info=vuln_info,
                                                                 scopen=scopen,
                                                                 fix=fix,
                                                                 vuln_asset = asset,
                                                                 )
            vuln = res[0]
            if vuln.vuln_id == vuln_id:
                if vuln.fix_status == '1':
                    vuln.fix_status= '3'
            else:
                vuln.vuln_id = vuln_id
                if leave == '0':
                    vuln.fix_status= '0'
                vuln.fix_status= '2'
            vuln.save()
            error='添加成功'
        else:
            error = '请检查输入'
    else:
        form = forms.Vuln_edit_form()
    return render(request,'formupdate.html',{'form':form,'post_url':'vulncreate','argu':asset_id,'error':error})


@login_required
def vulndetails(request,vuln_id):
    user = request.user
    if user.is_superuser:
        vuln = get_object_or_404(models.Vulnerability_scan,vuln_id=vuln_id)
    else:
        vuln = get_object_or_404(models.Vulnerability_scan,vuln_asset__asset_user=user,vuln_id=vuln_id)
    return render(request,'VulnManage/vulndetails.html',{'vuln':vuln})



@login_required
def vulnview(request):
    
    return render(request,'VulnManage/vulnlist.html')




@login_required
@csrf_protect
def vulntablelist(request):
    user = request.user
    resultdict={}
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    key = request.POST.get('key')
    if  not key:
        key=''
    
    leave = request.POST.get('leave')
    if  not leave:
        leave=''
    fix_status = request.POST.get('fix_status')
    if  not fix_status:
        fix_status=''
    
    
    if user.is_superuser:
        vuln_list = models.Vulnerability_scan.objects.filter(
            vuln_asset__asset_key__icontains = key,
            leave__icontains = leave,
            fix_status__icontains = fix_status,
            leave__gte = 1,
            ).order_by('-fix_status','-leave')
    else:
        vuln_list = models.Vulnerability_scan.objects.filter(
            vuln_asset__asset_user=user,
            vuln_asset__asset_key__icontains = key,
            leave__icontains = leave,
            fix_status__icontains = fix_status,
            leave__gte = 1,
            ).order_by('-fix_status','-leave')
        
    total = vuln_list.count()
    vuln_list = paging(vuln_list,rows,page)
    data = []
    for vuln_item in vuln_list:
        dic={}
        dic['vuln_id'] =escape( vuln_item.vuln_id)
        dic['cve_name'] =escape( vuln_item.cve_name)
        dic['vuln_name'] =escape( vuln_item.vuln_name)
        dic['vuln_type'] =escape( vuln_item.vuln_type)
        dic['leave'] =escape( VULN_LEAVE[vuln_item.leave])
        dic['fix_status'] =escape( VULN_STATUS[vuln_item.fix_status])
        dic['update_data'] =escape( vuln_item.update_data)
        dic['asset'] =escape( vuln_item.vuln_asset.asset_key)
        dic['asset_id'] =escape( vuln_item.vuln_asset.asset_id)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="漏洞列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)
        

@login_required
@csrf_protect
def vulnfixlist(request):
    user = request.user
    error =''
    vuln_id_list = request.POST.get('vuln_id_list')
    vuln_id_list = json.loads(vuln_id_list)
    action = request.POST.get('action')
    if action == 'status':
        for vuln_id in vuln_id_list:
            if user.is_superuser:
                vuln = get_object_or_404(models.Vulnerability_scan,vuln_id=vuln_id)
                vuln.fix_status='4'
            else:
                vuln = get_object_or_404(models.Vulnerability_scan,asset_user=user,vuln_id=vuln_id)
                vuln.fix_status='4'
            vuln.save()
        error = '操作成功'
    else:
        error ='参数错误'
    return JsonResponse({'error':error})   