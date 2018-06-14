#coding:utf-8
'''
Created on 2018年5月25日

@author: yuguanc
'''

from __future__ import absolute_import
from celery import shared_task
from SeMFSetting.Functions import Nessus,AWVS11
from TaskManage.Functions import nessus,awvs
import time
from TaskManage.models import Task
from NoticeManage.views import notice_add

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from SeMFSetting.Functions.mails import send_notice_mail


@shared_task
def save_scan_vulns(scan_id,task_id):
    task = Task.objects.filter(task_id =task_id ).first()
    while True:
        res = Nessus.details(scan_id,task.task_scanner.id)
        try:
            res['info']['status']
        except:
            continue
        if res['info']['status'] == 'canceled' or res['info']['status'] == 'completed' or res['info']['status'] == 'stopping' :
            #time.sleep(600)
            nessus.get_scan_vuln(scan_id,task,task.task_scanner.id)
            task.task_status=4
            task.save()
            data={
                  'notice_title':'任务进度通知',
                  'notice_body':'您对'+task.task_name+'的扫描任务已完成，请及时查看结果',
                  'notice_url':'/task/user/',
                  'notice_type':'notice',
                  }
            user = task.task_user
            notice_add(user,data)
            send_notice_mail(user.email,data)
            break
        else:
            time.sleep(30)
            
            
@shared_task
def save_awvs_vulns(scan_id,task_id):
    task = Task.objects.filter(task_id =task_id ).first()
    while True:
        status = AWVS11.getstatus(scan_id,task.task_scanner.id)
        if status == 'completed':
            awvs.get_scan_result(scan_id,task_id,task.task_scanner.id)
            task.task_status=4
            task.save()
            #type_task_list = {'移动应用':'type1','web应用':'type2','操作系统':'type3'}
            data={
                  'notice_title':'任务进度通知',
                  'notice_body':'您对'+task.task_name+'的扫描任务已完成，请及时查看结果',
                  'notice_url':'/task/user/',
                  'notice_type':'notice',
                  }
            user = task.task_user
            notice_add(user,data)
            send_notice_mail(user.email,data)
            break
        elif status == 'aborted':
            awvs.get_scan_result(scan_id,task_id,task.task_scanner.id)
            task.task_status=5
            task.save()
            #type_task_list = {'移动应用':'type1','web应用':'type2','操作系统':'type3'}
            data={
                  'notice_title':'任务进度通知',
                  'notice_body':'您对'+task.task_name+'的扫描任务已完成，请及时查看结果',
                  'notice_url':'/task/user/',
                  'notice_type':'notice',
                  }
            user = task.task_user
            notice_add(user,data)
            send_notice_mail(user.email,data)
            break
        else:
            time.sleep(60)