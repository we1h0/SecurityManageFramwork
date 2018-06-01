#coding:utf-8
'''
Created on 2018年5月25日

@author: yuguanc
'''
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .. import models,forms
from ..Functions import nessus
from AssetManage.models import Asset
import time
from ..tasks import save_scan_vulns


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
            task_scanner=form.cleaned_data['task_scanner']
            task_targetinfo=form.cleaned_data['task_targetinfo']
            
            if user.is_superuser:
                asset_list = Asset.objects.filter(asset_type__parent__name = '网络设备')
            else:
                asset_list = Asset.objects.filter(asset_type__parent__name = '网络设备',asset_user=user)
                
            task_target =''
            for item in asset_list:
                task_target = task_target + item.asset_key +';'
            scan_id = nessus.add_nessus_scan(task_name,task_targetinfo,task_target,task_scanner.id)
            
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
                task_target=task_target,
                task_targetinfo=task_targetinfo,
                request_status=request_status,
                task_status=task_status,
                task_user=user
                )
            task_get = task_get[0]
            asset_list = models.Asset.objects.filter()
            for asset in asset_list:
                task_get.task_asset.add(asset)
            task_get.task_user = user
            task_get.save()
            error = '添加成功'
    else:
        form = forms.TaskCreateForm()
    return render(request,'formedit.html',{'form':form,'post_url':'nessusscanall','error':error})




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
            nessus_scan.task_status=2
            nessus_scan.save()
            save_scan_vulns.delay(scan_id,task.id)
            #save_scan_vulns(scan_id,task)
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