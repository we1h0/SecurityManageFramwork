#coding:utf-8
'''
Created on 2018年5月25日

@author: yuguanc
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .. import models,forms
from ..Functions import nessus,awvs
from AssetManage.models import Asset
import time
from ..tasks import save_scan_vulns,save_awvs_vulns

@login_required
@csrf_protect
def scan_task(request,action='post'):
    user=request.user
    error =''
    if request.method=='GET':
        asset_id_list = action
        asset_id_list=asset_id_list.split(';')
        if len(asset_id_list) == 0:
            error = '未选择符合要求资产，请手动输入资产'
        elif len(asset_id_list) >= 16:
            error='所选资产超过最大值，请分批进行扫描'
        else:
            error= '被扫描资产已指定，可进行手动编辑'
        task_target =''
        for asset_id in asset_id_list:
            asset=Asset.objects.filter(asset_id=asset_id).first()
            if asset:
                task_target = task_target + asset.asset_key +','
        form = forms.TaskScanForm(initial={'task_target':task_target})
    elif request.method=='POST':
        form = forms.TaskScanForm(request.POST)
        if form.is_valid():
            try:
                num_id =models.Task.objects.latest('id').id
            except:
                num_id = 0
            num_id += 1
            task_id= str('s') + time.strftime('%Y%m%d',time.localtime(time.time())) + str(num_id)
            task_name=form.cleaned_data['task_name']
            #task_scanner=form.cleaned_data['task_scanner']
            scanner_police=form.cleaned_data['scanner_police']
            task_scanner=scanner_police.scanner
            task_target=form.cleaned_data['task_target']
            task_targetinfo=form.cleaned_data['task_targetinfo']
            if task_scanner.scanner_type == 'Nessus':
                scan_id = nessus.add_nessus_scan(task_name,task_targetinfo,task_target,task_scanner.id,scanner_police.policies_name)
                if user.is_superuser:
                    request_status='0'
                    task_status ='1'
                else:
                    request_status= '1'
                    task_status ='0'
                task_get=models.Task.objects.get_or_create(
                    task_id=task_id,
                    task_name=task_name,
                    scan_id=scan_id,
                    task_type = '安全扫描',
                    task_scanner=task_scanner,
                    scanner_police=scanner_police,
                    task_target=task_target,
                    task_targetinfo=task_targetinfo,
                    request_status=request_status,
                    task_status=task_status,
                    task_user=user
                    )
                task_get = task_get[0]
                task_get.task_user = user
                if user.is_superuser:
                    task_get.action_user=user
                task_get.save()
                error = '添加成功'
            else:
                error = '扫描节点不支持巡检'
    else:
        error ='请检查参数'
        return render(request,'error.html',{'error':error})
    return render(request,'TaskManage/taskupdate.html',{'form':form,'post_url':'taskscanchoice','argu':'post','error':error})
    
    
    
    
@login_required
@csrf_protect
def ScanAll(request):
    user = request.user
    error = ''
    
    if request.method == 'POST':
        form = forms.TaskCreateForm(request.POST)
        if form.is_valid():
            try:
                num_id =models.Task.objects.latest('id').id
            except:
                num_id = 0
            num_id += 1
            task_id= str('s') + time.strftime('%Y%m%d',time.localtime(time.time())) + str(num_id)
            task_name=form.cleaned_data['task_name']
            #task_scanner=form.cleaned_data['task_scanner']
            scanner_police=form.cleaned_data['scanner_police']
            task_scanner=scanner_police.scanner
            task_target=form.cleaned_data['task_target']
            task_targetinfo=form.cleaned_data['task_targetinfo']
            
            '''
            if user.is_superuser:
                asset_list = Asset.objects.filter(asset_type__parent__name = '网络设备')
            else:
                asset_list = Asset.objects.filter(asset_type__parent__name = '网络设备',asset_user=user)
            
            
            task_target =''
            for item in asset_list:
                task_target = task_target + item.asset_key +';'
            '''
            if user.is_superuser:
                task_asset = Asset.objects.filter(asset_key =task_target).first()
            else:
                task_asset = Asset.objects.filter(asset_key =task_target,asset_user=user).first()
            if task_asset:
                if task_asset.asset_type in task_scanner.assetType.all():
                    if task_scanner.scanner_type=='Nessus':
                        scan_id = nessus.add_nessus_scan(task_name,task_targetinfo,task_target,task_scanner.id,scanner_police.policies_name)
                    elif task_scanner.scanner_type=='AWVS':
                        scan_id = awvs.add_scan(task_scanner.id, task_target, task_targetinfo)
                    if scan_id !='error':
                        if user.is_superuser:
                            request_status='0'
                            task_status ='1'
                        else:
                            request_status= '1'
                            task_status ='0'
                        task_get=models.Task.objects.get_or_create(
                            task_id=task_id,
                            task_name=task_name,
                            scan_id=scan_id,
                            task_type = '安全扫描',
                            task_scanner=task_scanner,
                            scanner_police=scanner_police,
                            task_target=task_target,
                            task_targetinfo=task_targetinfo,
                            request_status=request_status,
                            task_status=task_status,
                            task_user=user
                            )
                        task_get = task_get[0]
                        task_get.task_asset.add(task_asset)
                        task_get.task_user = user
                        if user.is_superuser:
                            task_get.action_user=user
                        task_get.save()
                        error = '添加成功'
                    else:
                        error = '请检查任务目标格式'
                else:
                    error = '该策略不适合被扫描资产'
            else:
                error = '扫描目标不在资产列表中'
    else:
        form = forms.TaskCreateForm()
    return render(request,'TaskManage/taskedit.html',{'form':form,'post_url':'scantask','error':error})




def sys_action(request,task,action):
    nessus_scan = task
    scanner_id = task.task_scanner.id
    error = None
    if action == 'run':
        scan_id = nessus_scan.scan_id
        if nessus_scan.task_type == '安全扫描':
            do_res = nessus.launch_nessus_scan(scan_id,scanner_id)
        else:
            do_res = True
        if do_res:
            save_scan_vulns.delay(scan_id,task.task_id)
            #save_scan_vulns(scan_id,task)
            nessus_scan.task_status=2
            nessus_scan.save()
        else:
            error = '操作失误，请重试'
    elif action == 'pause':
        scan_id = nessus_scan.scan_id
        do_res = nessus.pause_nessus_scan(scan_id,scanner_id)
        if do_res:
            nessus_scan.task_status=3
            nessus_scan.save()
        else:
            error = '操作失误，请重试'
    elif action == 'stop':
        scan_id = nessus_scan.scan_id
        do_res = nessus.stop_nessus_scan(scan_id,scanner_id)
        if do_res:
            nessus_scan.task_status=5
            nessus_scan.save()
        else:
            error = '操作失误，请重试'
    elif action == 'resume':
        scan_id = nessus_scan.scan_id
        do_res = nessus.resume_nessus_scan(scan_id,scanner_id)
        if do_res:
            nessus_scan.task_status=2
            nessus_scan.save()
        else:
            error = '操作失误，请重试'
    else:
        error = '错误操作指令'
    if error:
        return error
    else:
        return True
    
    
def web_action(request,task,action):
    web_scan = task
    if action == 'run':
        target_id = web_scan.scan_id
        scan_id = awvs.start_scan(task.task_scanner.id,target_id)
        web_scan.task_status=2
        web_scan.scan_id=scan_id
        web_scan.save()
        save_awvs_vulns.delay(scan_id,task.task_id)
        #save_awvs_vulns(scan_id,task)
    elif action == 'stop':
        scan_id = web_scan.scan_id
        res = awvs.stop_scan(scan_id,task.task_scanner.id)
        if res:
            web_scan.task_status=5
        web_scan.save()
    else:
        error = '该类任务暂不支持暂停，请选择取消任务'
        return render(request,'error.html',{'error':error})
    return True