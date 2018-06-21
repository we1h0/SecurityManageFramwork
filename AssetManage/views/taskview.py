#coding:utf-8
'''
Created on 2018年5月24日

@author: yuguanc
'''
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .. import tasks,models,forms
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
    



@login_required
@csrf_protect
def task_action(request):
    user = request.user
    error = ''
    asset_id_list = request.POST.get('asset_id_list')
    asset_id_list = json.loads(asset_id_list)
    if len(asset_id_list) == 0:
        error = '未选择符合要求资产'
    else:
        action = request.POST.get('action')
        if action == 'port':
            tasks.asset_port.delay(user.id,asset_id_list)
            error = '任务已提交'
        elif  action == 'segment':
            tasks.asset_descover.delay(user.id,asset_id_list)
            error = '任务已提交'
        else:
            error = '参数错误'
    return JsonResponse({'error':error})


@login_required
@csrf_protect
def assetuser_action(request):
    user = request.user
    asset_id_list = request.POST.get('asset_id_list')
    asset_user = models.AssetUser.objects.get_or_create(
        asset_list=asset_id_list,
        action_user=user,
        )
    assetuser_id = asset_user[0].id
    return JsonResponse({'assetuser_id':assetuser_id})

@login_required
@csrf_protect
def assetuser(request,assetuser_id):
    user = request.user
    error = ''
    assetuser = get_object_or_404(models.AssetUser,id =assetuser_id,action_user=user )
    if request.method=='POST':
        form = forms.AssetUserForm(request.POST,instance=assetuser)
        if form.is_valid():
            dst_user_email = form.cleaned_data['dst_user_email']
            user = User.objects.filter(email = dst_user_email).first()
            if user:
                asset_id_list = form.cleaned_data['asset_list']
                asset_id_list = json.loads(asset_id_list)
                form.save()
                tasks.asset_user_save.delay(dst_user_email, asset_id_list)
                error='操作成功'
            else:
                error ='对方账号不存在'
        else:
            errro = '请检查输入'
    else:
        form = forms.AssetUserForm(instance=assetuser)
    return render(request,'formupdate.html',{'form':form,'post_url':'assetuserdo','argu':assetuser_id,'error':error})

    