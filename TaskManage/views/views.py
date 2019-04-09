#coding:utf-8

# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from SeMFSetting.views import paging
from django.http import JsonResponse
from .. import models,forms
from TaskManage.views.Scantasks import sys_action,web_action
import time
from django.utils.html import escape


TASK_STATUS={
        '0':'审批中',
        '1':'待执行',
        '2':'执行中',
        '3':'已暂停',
        '4':'已完成',
        '5':'已结束',
        }


@login_required
@csrf_protect
def taskrequestaction(request,task_id,action):
    user = request.user
    error=''
    
    if user.is_superuser:
        task = get_object_or_404(models.Task,task_id=task_id)
        if action =='access':
            task.task_status = '1'
            task.request_status = '1'
            task.request_note = '已验证'
            task.action_user=user
        elif action == 'deny':
            task.task_status = '5'
            task.request_status = '2'
            task.action_user=user
        task.save()
        error = '审批完成'
    else:
        error = '权限错误'
    return JsonResponse({'error':error})
            
        
    



@login_required
def taskdetails(request,task_id):
    user = request.user
    if user.is_superuser:
        task = get_object_or_404(models.Task,task_id=task_id)
    else:
        task = get_object_or_404(models.Task,task_user=user,task_id=task_id)
    return render(request,'TaskManage/taskdetails.html',{'task':task})



@login_required
@csrf_protect
def TaskRequestView(request):
    return render(request,'TaskManage/taskrequest.html')


@login_required
@csrf_protect
def taskrequesttablelist(request):
    user = request.user
    resultdict={}
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    if user.is_superuser:
        task_list = models.Task.objects.filter(task_status=0).order_by('task_starttime')
        total = task_list.count()
        task_list = paging(task_list,rows,page)
        data = []
        for item in task_list:
            dic={}
            dic['task_id'] =escape( item.task_id)
            dic['task_name'] =escape( item.task_name)
            dic['task_type'] =escape( item.task_type)
            dic['task_target'] =escape( item.task_target)
            dic['task_starttime'] =escape( item.task_starttime)
            dic['task_scanner'] =escape( item.task_scanner.scanner_name)
            dic['task_user'] =escape( item.task_user.email)
            data.append(dic)
        resultdict['code']=0
        resultdict['msg']="任务列表"
        resultdict['count']=total
        resultdict['data']=data
        return JsonResponse(resultdict)



@login_required
def task_action(request,task_id,action):
    user = request.user
    if user.is_superuser:
        task =models.Task.objects.exclude(task_status=0).filter(task_status__lt=4,task_id = task_id).first()
    else:
        task = user.task_for_user.exclude(task_status=0).filter(task_status__lt=4,request_status='1',task_id = task_id).first()
    if task:
        if task.task_scanner.scanner_type == 'Nessus':
            res = sys_action(request,task,action)
            if res:
                error ='执行成功'
            else:
                error = '操作失误，请联系管理员'
        elif task.task_scanner.scanner_type == 'AWVS':
            res = web_action(request,task,action)
            if res:
                error ='执行成功'
            else:
                error = '操作失误，请联系管理员'
        elif task.task_scanner.scanner_type == 'MobSF':
            error = '暂未提供该类任务'
    else:
        error = '请不要随意更改参数哦，会被记住的'
    return JsonResponse({'error':error})

@login_required
@csrf_protect
def TaskSync(request):
    user = request.user
    error = ''
    if user.is_superuser:
        if request.method == 'POST':
            form = forms.TaskSyncForm(request.POST,request.FILES)
            if form.is_valid():
                task_scanner = form.cleaned_data['task_scanner']
                if task_scanner.scanner_type == 'Nessus':
                    try:
                        num_id =models.Task.objects.latest('id').id
                    except:
                        num_id = 0
                    num_id += 1
                    task_id = str('s') + time.strftime('%Y%m%d',time.localtime(time.time())) + str(num_id)
                    task_name = form.cleaned_data['task_name']
                    task_type = '扫描同步'
                    
                    scan_id = form.cleaned_data['scan_id']
                    task_targetinfo = form.cleaned_data['task_targetinfo']
                    
                    models.Task.objects.get_or_create(
                        task_id=task_id,
                        task_name=task_name,
                        task_type=task_type,
                        task_scanner=task_scanner,
                        scan_id=scan_id,
                        task_status ='1',
                        task_user = user,
                        task_targetinfo=task_targetinfo
                        )
                    error = '创建成功'
                else:
                    error = '扫描节点不支持导入'
        else:
            form = forms.TaskSyncForm()
        return render(request,'formedit.html',{'form':form,'post_url':'tasksync','error':error})
    else:
        error = '权限错误'
    return render(request,'error.html',{'error':error})





@login_required
@csrf_protect
def TaskView(request):
    return render(request,'TaskManage/tasklist.html')


@login_required
@csrf_protect
def tasktablelist(request):
    user = request.user
    resultdict={}
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    name = request.POST.get('name')
    if  not name:
        name=''
    
    key = request.POST.get('key')
    if  not key:
        key=''
        
    tasktype = request.POST.get('type')
    if  not tasktype:
        tasktype=['安全扫描','扫描同步']
    else:
        tasktype = [tasktype]
        
    taskstatus = request.POST.get('status')
    if  not taskstatus:
        if user.is_superuser:
            taskstatus=['1','2','3','4','5']
        else:
            taskstatus=['0','1','2','3','4','5']
    else:
        taskstatus = [taskstatus]
        
    
    if user.is_superuser:
        task_list = models.Task.objects.filter(
            task_name__icontains = name,
            task_type__icontains = key,
            task_type__in = tasktype,
            task_status__in = taskstatus
            ).order_by('task_status','-task_endtime')
    else:
        task_list = models.Task.objects.filter(
            task_user = user,
            task_name__icontains = name,
            task_type__icontains = key,
            task_type__in = tasktype,
            task_status__in = taskstatus
            ).order_by('task_status','-task_endtime')
        
    total = task_list.count()
    task_list = paging(task_list,rows,page)
    data = []
    for item in task_list:
        dic={}
        dic['task_id'] =escape( item.task_id)
        dic['task_name'] =escape( item.task_name)
        dic['task_type'] =escape( item.task_type)
        dic['task_target'] =escape( item.task_target)
        dic['task_status'] =escape( TASK_STATUS[item.task_status])
        dic['task_starttime'] =escape( item.task_starttime)
        dic['task_scanner'] =escape( item.task_scanner.scanner_name)
        dic['task_user'] =escape( item.task_user.email)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="任务列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)