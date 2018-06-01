#coding:utf-8
'''
Created on 2018年5月25日

@author: yuguanc
'''

from __future__ import absolute_import
from celery import shared_task
from SeMFSetting.Functions import Nessus
from TaskManage.Functions import nessus
import time
from TaskManage.models import Task
from NoticeManage.views import notice_add

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from SeMFSetting.Functions.mails import send_notice_mail


@shared_task
def save_scan_vulns(scan_id,task_id):
    task = Task.objects.filter(id =task_id ).first()
    while True:
        res = Nessus.details(scan_id,task.task_scanner.id)
        if res['info']['status'] == 'canceled' or res['info']['status'] == 'completed' or res['info']['status'] == 'stopping' :
            #time.sleep(600)
            nessus.get_scan_vuln(scan_id,task,task.task_scanner.id)
            task.task_status=4
            task.save()
            data={
                  'notice_title':'任务进度通知',
                  'notice_body':'您对'+task.task_id+'的扫描任务已完成，请及时查看结果',
                  'notice_url':'/task/user/',
                  'notice_type':'notice',
                  }
            user = task.task_user
            notice_add(user,data)
            send_notice_mail(user.email,data)
            break
        else:
            time.sleep(30)