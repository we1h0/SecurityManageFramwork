#coding:utf-8
'''
Created on 2018年6月6日

@author: yuguanc
'''
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .. import models,forms
from django.contrib.auth.models import User
from NoticeManage.views import notice_add
from django.http import JsonResponse
from SeMFSetting.views import paging
from django.db.models import Q
from django.utils.html import escape

REQUEST_STATUS={
    '0':'待审批',
    '1':'待审通过',
    '2':'审批拒绝',
    }


@login_required
@csrf_protect
def asset_handover_action(request):
    user  = request.user
    error = ''
    action = request.POST.get('action')
    asset_handover_id = request.POST.get('asset_handover_id')
    asset_handover = get_object_or_404(models.Handover,id=asset_handover_id)
    dst_user = User.objects.filter(email=asset_handover.dst_email).first()
    request_user = User.objects.filter(email=asset_handover.request_user).first()
    if asset_handover.status =='0':
        if action == 'access':
            asset_handover.status = '1'
            asset_list = models.Asset.objects.filter(asset_user = request_user)
            for asset in asset_list:
                asset.asset_user.remove(request_user)
                asset.asset_user.add(dst_user)
                asset.save()
            request_user.is_active = False
            request_user.save()
        else:
            asset_handover.status = '2'
        asset_handover.action_user = user
        asset_handover.save()
        data_manage={
                      'notice_title':'资产交接通知',
                      'notice_body':user.username+'对'+asset_handover.request_user+'的申请已进行审批',
                      'notice_url':'/asset/handover/',
                      'notice_type':'notice',
                      }
        user_manage_list = User.objects.filter(is_superuser=True)
        for user_manage in user_manage_list:
            notice_add(user_manage,data_manage)
        error = '审批完成'
    else:
        error = '请勿重复审批'
    return JsonResponse({'error':error})



@login_required
def asset_handover_list(request):
    user  = request.user
    if user.is_superuser:
        resultdict={}
        
        page = request.POST.get('page')
        rows = request.POST.get('limit')
        
        email = request.POST.get('email')
        if not email:
            email = ''
        
        status = request.POST.get('status')
        if not status:
            status = ['0','1','2']
        else:
            status = [status]
        
        handover_list = models.Handover.objects.filter(status__in = status).filter(
            Q(dst_email__icontains = email)|
            Q(request_user__icontains = email)
            ).order_by('status','-request_starttime')
        
        total = handover_list.count()
        handover_list = paging(handover_list,rows,page)
        data = []
        for handover in handover_list:
            dic={}
            dic['id']=escape(handover.id)
            dic['request_user']=escape(handover.request_user)
            dic['dst_email']=escape(handover.dst_email)
            dic['reason']=escape(handover.reason)
            dic['status']=escape(REQUEST_STATUS[handover.status])
            dic['request_updatetime']=escape(handover.request_updatetime)
            data.append(dic)
        resultdict['code']=0
        resultdict['msg']="端口列表"
        resultdict['count']=total
        resultdict['data']=data
        return JsonResponse(resultdict)
    else:
        error = '权限错误'
    return JsonResponse({'error':error})

@login_required
def handoverview(request):
    return render(request,'AssetManage/assethandoverlist.html')

@login_required
@csrf_protect
def asset_handover(request):
    user = request.user
    error = ''
    if request.method =='POST':
        form = forms.HandoverForm(request.POST)
        if form.is_valid():
            dst_email = form.cleaned_data['dst_email']
            reason = form.cleaned_data['reason']
            dst_user = User.objects.filter(email=dst_email).first()
            if dst_user:
                models.Handover.objects.get_or_create(
                    dst_email=dst_email,
                    reason=reason,
                    request_user=user.email
                    )
                data={
                      'notice_title':'资产转让通知',
                      'notice_body':'您的资产申请已提交，转让对象为'+dst_email,
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
                data_manage={
                      'notice_title':'资产转让通知',
                      'notice_body':user.username+'提交资产转让申请，请进行核实' ,
                      'notice_url':'/asset/manage/handoverlist/',
                      'notice_type':'notice',
                      }
                notice_add(user,data)
                user_manage_list = User.objects.filter(is_superuser=True)
                for user_manage in user_manage_list:
                    notice_add(user_manage,data_manage)
                error= '申请已提交，审批通过后会邮件提醒'
            else:
                error = '转交目标不存在，请通知对方注册账号'
        else:
            error = '请检查输入'
    else:
        form = forms.HandoverForm()
    return render(request,'formedit.html',{'form':form,'post_url':'assethandover','error':error})
                
                