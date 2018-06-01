#coding:utf-8
'''
Created on 2018年5月18日

@author: yuguanc
'''
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .. import models,forms
from django.http import JsonResponse

@login_required
@csrf_protect
def plugincreate(request,asset_id):
    user = request.user
    error =''
    if user.is_superuser:
        asset = get_object_or_404(models.Asset,asset_id=asset_id)
    else:
        asset = get_object_or_404(models.Asset,asset_user = user,asset_id=asset_id)
    if request.method == 'POST':
        form = forms.Asset_plugin_info(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            version = form.cleaned_data['version']
            plugin_info = form.cleaned_data['plugin_info']
            models.Plugin_Info.objects.get_or_create(
                name=name,
                version=version,
                plugin_info=plugin_info,
                asset=asset
                )
            error='添加成功'
        else:
            error = '请检查输入'
    else:
        form = forms.Asset_plugin_info()
    return render(request,'formupdate.html',{'form':form,'post_url':'plugincreate','argu':asset_id,'error':error})


@login_required
@csrf_protect
def pluginupdate(request,plugin_id):
    user = request.user
    error =''
    if user.is_superuser:
        plugin = get_object_or_404(models.Plugin_Info,id=plugin_id)
    else:
        plugin = get_object_or_404(models.Plugin_Info,asset__asset_user = user,id=plugin_id)
    if request.method == 'POST':
        form = forms.Asset_plugin_info(request.POST,instance =plugin)
        if form.is_valid():
            form.save()
            error='添加成功'
        else:
            error = '请检查输入'
    else:
        form = forms.Asset_plugin_info(instance =plugin)
    return render(request,'formupdate.html',{'form':form,'post_url':'pluginupdate','argu':plugin_id,'error':error})


@login_required
def plugindelete(request,plugin_id):
    user = request.user
    error =''
    if user.is_superuser:
        plugin = get_object_or_404(models.Plugin_Info,id=plugin_id)
    else:
        plugin = get_object_or_404(models.Plugin_Info,asset__asset_user = user,id=plugin_id)
    if plugin:
        plugin.delete()
        error = '删除成功'
    else:
        error = '非法参数'
    return JsonResponse({'error':error})

