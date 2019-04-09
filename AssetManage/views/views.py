#coding:utf-8

from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .. import models,forms
from django.contrib.auth.models import User
from SeMFSetting.views import paging
from django.http import JsonResponse
from RBAC.models import Area
import json,time,random
from django.utils.html import escape
# Create your views here.
ASSET_STATUS={
    '0':'使用中',
    '1':'闲置中',
    '2':'已销毁',
    }

REQUEST_STATUS={
    '0':'待审批',
    '1':'待审通过',
    '2':'审批拒绝',
    }





@login_required
@csrf_protect
def asset_request_list_action(request):
    user = request.user
    error =''
    if user.is_superuser:
        request_id_list = request.POST.get('request_id_list')
        request_id_list=json.loads(request_id_list)
        action = request.POST.get('action')
        if action =='deny':
            for request_id in request_id_list:
                assetrequest = get_object_or_404(models.AssetRequest,id = request_id)
                if assetrequest.asset_request_status != '0':
                    pass
                else:
                    assetrequest.asset_request_status= '2'
                    assetrequest.action_user = user
                    assetrequest.save()
            error = '已审批'
        elif action =='access' :
            for request_id in request_id_list:
                assetrequest = get_object_or_404(models.AssetRequest,id = request_id)
                if assetrequest.asset_request_status != '0':
                    pass
                else:
                    assetrequest.asset_request_status= '1'
                    assetrequest.action_user = user
                    asset= get_object_or_404(models.Asset,asset_key = assetrequest.asset_key)
                    asset.asset_user.add(assetrequest.request_user)
                    asset.user_email = assetrequest.request_user.email
                    asset.asset_inuse=True
                    asset.save()
                    assetrequest.save()
            error = '已审批'
        else:
            error ='参数错误'
        
    else:
        error = '权限错误'
    return JsonResponse({'error':error})


@login_required
@csrf_protect
def assetrequestaction(request):
    user = request.user
    error =''
    if user.is_superuser:
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        requestlist = get_object_or_404(models.AssetRequest,id = request_id)
        if requestlist.asset_request_status !='0':
            error = '请勿重复审批'
        else:
            if action == 'access':
                requestlist.asset_request_status= '1'
                requestlist.action_user = user
                asset= get_object_or_404(models.Asset,asset_key = requestlist.asset_key)
                asset.asset_user.add(requestlist.request_user)
                asset.user_email = requestlist.request_user.email
                asset.save()
                requestlist.save()
                error = '已审批'
            elif action == 'deny':
                requestlist.asset_request_status= '2'
                requestlist.action_user = user
                requestlist.save()
                error = '已审批'
            else:
                error ='未指定操作'
    else:
        error ='权限错误'
    return JsonResponse({'error':error})




@login_required
@csrf_protect
def assetreqeustlist(request):
    user = request.user
    resultdict={}
    
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    email = request.POST.get('email')
    if  not email:
        email=''
    status = request.POST.get('status')
    if not status:
        status='' 
    
    
    if user.is_superuser:
        request_list = models.AssetRequest.objects.filter(request_user__email__icontains=email,asset_request_status__icontains=status).order_by('asset_request_status','request_starttime')
    else:
        request_list = user.assetrequest_for_user.filter(request_user__email__icontains=email,asset_request_status__icontains=status).order_by('asset_request_status','request_starttime')
    total = request_list.count()
    request_list = paging(request_list,rows,page)
    data = []
    for request_item in request_list:
        dic={}
        dic['request_id'] = escape(request_item.id)
        dic['asset_key'] = escape(request_item.asset_key)
        dic['asset_type'] = escape(request_item.asset_type.name)
        dic['asset_request_status'] = escape(REQUEST_STATUS[request_item.asset_request_status])
        dic['request_action'] = escape(request_item.request_action)
        dic['request_user'] = escape(request_item.request_user.username)
        dic['request_reason'] = escape(request_item.request_reason)
        dic['request_starttime'] = escape(request_item.request_starttime)
        if request_item.action_user:
            dic['action_user'] = escape(request_item.action_user.username)
            dic['request_updatetime'] = escape(request_item.request_updatetime)
        else:
            dic['action_user'] = ''
            dic['request_updatetime'] = ''
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="用户列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)   


@login_required
def assetrequestview(request):
    return render(request,'AssetManage/assetrequestlist.html')



@login_required
@csrf_protect
def asset_request(request):
    user = request.user
    error = ''
    if request.method == 'POST':
        form = forms.AssetRequest_edit_form(request.POST)
        if form.is_valid():
            asset_key= form.cleaned_data['asset_key']
            asset = models.Asset.objects.filter(asset_key=asset_key)
            if asset:
                asset_type = form.cleaned_data['asset_type']
                request_action = form.cleaned_data['request_action']
                request_reason = form.cleaned_data['request_reason']
                asset_request = models.AssetRequest.objects.get_or_create(
                    asset_key = asset_key,
                    asset_type=asset_type,
                    request_action=request_action,
                    request_reason=request_reason,
                    request_user=user
                    )
                error = '申请已提交，请等待审批'
            else:
                error = '资产库内无该资产，请使用资产新增'
        else:
            error ='请检查输入'
        return render(request,'formedit.html',{'form':form,'post_url':'assetrequest','error':error})
    else:
        form = forms.AssetRequest_edit_form()
    return render(request,'formedit.html',{'form':form,'post_url':'assetrequest'})


@login_required
@csrf_protect
def asset_create(request):
    user = request.user
    error = ''
    if request.method == 'POST':
        form = forms.Asset_create_form(request.POST)
        if form.is_valid():
            try:
                num_id =models.Asset.objects.latest('id').id
            except:
                num_id = 0
            num_id += 1
            asset_id = '01' + time.strftime('%Y%m%d',time.localtime(time.time()))+str(num_id)
            asset_name = form.cleaned_data['asset_name']
            asset_type = form.cleaned_data['asset_type']
            asset_key = form.cleaned_data['asset_key']
            asset_area = form.cleaned_data['asset_area']
            user_email = form.cleaned_data['user_email']
            asset_out_id = form.cleaned_data['asset_out_id']
            asset_description = form.cleaned_data['asset_description']
            asset_create = models.Asset.objects.get_or_create(
                asset_id=asset_id,
                asset_name=asset_name,
                asset_type=asset_type,
                asset_key=asset_key,
                asset_area=asset_area,
                asset_out_id=asset_out_id,
                asset_description=asset_description,
                )
            if asset_create[1]:
                asset = asset_create[0]
                if user.is_superuser:
                    asset.user_email = user_email
                    user_get = User.objects.filter(email = user_email).first()
                    if user_get:
                        asset.asset_inuse=True
                        asset.asset_user.add(user)
                    else:
                        asset.asset_inuse=False
                else:
                    asset.asset_inuse=True
                    if user_email:
                        asset.user_email = user_email
                    else:
                        asset.user_email = user.email
                    asset.asset_user.add(user)
                asset.save()
            error = '添加成功'
        else:
            error ='非法输入或资产已存在，请进行资产申请'
        return render(request,'formedit.html',{'form':form,'post_url':'assetcreate','error':error})
    else:
        form = forms.Asset_create_form()
    return render(request,'formedit.html',{'form':form,'post_url':'assetcreate'})





@login_required
@csrf_protect
def assetupdate(request,asset_id):
    user = request.user
    error =''
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user=user,asset_id=asset_id)
    if request.method == 'POST':
        form = forms.Asset_create_form(request.POST,instance=asset)
        if form.is_valid():
            form.save()
            error = '修改成功'
        else:
            error = '请检查输入'
    else:
        form = forms.Asset_create_form(instance=asset)
    return render(request,'formupdate.html',{'form':form,'post_url':'assetupdate','argu':asset_id,'error':error})


@login_required
@csrf_protect
def assetdelete(request):
    user = request.user
    error ='操作成功'
    asset_id_list = request.POST.get('asset_id_list')
    asset_id_list = json.loads(asset_id_list)
    action = request.POST.get('action')
    if action == 'delete':
        for asset_id in asset_id_list:
            if user.is_superuser:
                asset = get_object_or_404(models.Asset,asset_id=asset_id)
                asset.asset_status='2'
            else:
                asset = get_object_or_404(models.Asset,asset_user=user,asset_id=asset_id)
                asset.asset_inuse=False
                asset.asset_user.remove(user)
            asset.save()
    else:
        error ='参数错误'
    return JsonResponse({'error':error})
    



@login_required
def assetview(request):
    
    area = Area.objects.filter(parent__isnull=True)
    asset_type = models.AssetType.objects.filter(parent__isnull=False)
    
    return render(request,'AssetManage/assetlist.html',{'area':area,'asset_type':asset_type})



@login_required
@csrf_protect
def assettablelist(request):
    user= request.user
    resultdict={}
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    name = request.POST.get('name')
    if  not name:
        name=''
    key = request.POST.get('key')
    if  not key:
        key=''
        
    asset_type = request.POST.get('type')
    if not asset_type:
        type_get = models.AssetType.objects.filter(parent__isnull=False)
    else:
        type_get = models.AssetType.objects.filter(id =asset_type )
    '''
    area = request.POST.get('area')
    if not area:
        area_get = Area.objects.filter(parent__isnull=True)
    else:
        area_get = Area.objects.filter(id =area )'''
    
    
    if user.is_superuser:
        assetlist = models.Asset.objects.filter(
            asset_name__icontains = name,
            asset_key__icontains = key,
            asset_type__in=type_get,
            #asset_area__in=area_get,
            ).order_by('-asset_score','-asset_updatetime')
    else:
        assetlist = user.asset_to_user.all().order_by('-asset_score','-asset_updatetime')
        user_child_list = user.user_parent.all()
        for user_child in user_child_list:
            child_asset_list = user_child.asset_to_user.all().order_by('-asset_score','-asset_updatetime')
            assetlist = assetlist | child_asset_list
        assetlist.filter(
            asset_name__icontains = name,
            asset_key__icontains = key,
            asset_type__in=type_get,
            #asset_area__in=area_get,
            )
    total = assetlist.count()
    assetlist = paging(assetlist,rows,page)
    data = []
    for asset_item in assetlist:
        dic={}
        dic['asset_id'] = escape( asset_item.asset_id)
        dic['asset_name'] = escape( asset_item.asset_name)
        dic['asset_key'] = escape( asset_item.asset_key)
        dic['asset_status'] = escape( ASSET_STATUS[asset_item.asset_status])
        if asset_item.asset_inuse:
            dic['asset_inuse'] = escape( '已认领')
        else:
            dic['asset_inuse'] = escape( '待认领')
        if asset_item.asset_type:
            dic['asset_type'] = escape( asset_item.asset_type.name)
        else:
            dic['asset_type'] = escape( '未分类')
        dic['user_email'] = escape( asset_item.user_email)
        dic['asset_score'] = escape( asset_item.asset_score)
        dic['asset_updatetime'] = escape( asset_item.asset_updatetime)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="用户列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)
        
        
        
        
        
        
        
        
        
        
    