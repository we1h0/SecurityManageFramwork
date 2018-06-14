#coding:utf-8
'''
Created on 2017/12/4

@author: gy
'''

import time 

from SeMFSetting.Functions import AWVS11
from SeMFSetting.Functions import parse_awvs_xml
from VulnManage.models import Vulnerability_scan
from TaskManage.models import Task
from AssetManage.models import Asset
from SeMF.settings import TMP_PATH
from .nessus import Get_except_vuln

vuln_level = {'informational':0,'low':1,'medium':2,'high':3}


def add_scan(scanner_id,url,desc):
    target_id = AWVS11.add(url,scanner_id, desc)
    return target_id

def start_scan(scanner_id,target_id):
    data = AWVS11.start(target_id,scanner_id)
    if data:
        scan_id = AWVS11.getscanid(target_id,scanner_id)
    return scan_id

def stop_scan(scan_id,scanner_id):
    data = AWVS11.stop(scan_id,scanner_id)
    if data:
        return True

def dele_scan(scan_id,scanner_id):
    data = AWVS11.delete(scan_id,scanner_id)
    if data:
        return True

def get_scan_result(scan_id,task_id,scanner_id):
    reporturl = AWVS11.getreport(scan_id,scanner_id)
    task = Task.objects.filter(task_id=task_id).first()
    parse_awvs_xml.get_scan_xml(reporturl,scan_id,TMP_PATH)
    details = parse_awvs_xml.details_parse_xml(scan_id,TMP_PATH)
    if details:
        asset_key = details['starturl']
        vuln_list = details['bug']
        asset =Asset.objects.filter(asset_key = asset_key).first()
        if vuln_list:
            except_vuln,except_vuln_list = Get_except_vuln('AWVS')
            for vuln in vuln_list:
                try:
                    num = Vulnerability_scan.objects.latest('id').id
                except Exception as e:
                    num = 0
                vuln_id = '02' + str(time.strftime('%Y%m%d%H',time.localtime(time.time()))) +str( num)
                vuln_type = 'Awvs'
                vuln_name = vuln['name']
                leave = vuln_level[vuln['level']]
                vuln_info = vuln['request']
                introduce = vuln['details']
                scopen = vuln['path']
                fix = vuln['recommendation']
                if vuln_name in except_vuln:
                    vuln_gets = except_vuln_list.filter(vuln_name=vuln_name).first()
                    leave = vuln_gets.leave
                    fix = vuln_gets.fix
                vuln_list = Vulnerability_scan.objects.get_or_create(vuln_name=vuln_name,
                                                                     vuln_type=vuln_type,
                                                                     leave=leave,
                                                                     introduce=introduce,
                                                                     vuln_info=vuln_info,
                                                                     scopen=scopen,
                                                                     fix=fix,
                                                                     vuln_asset = asset
                                                                     )
                vuln_get = vuln_list[0]
                if vuln_get.vuln_id:
                    if vuln_get.fix_status == '1':
                        vuln_get.fix_status= '3'
                else:
                    vuln_get.vuln_id = vuln_id
                    if leave == 0:
                        vuln_get.fix_status= '0'
                    elif leave == 1:
                        vuln_get.fix_status= '0'
                    else:
                        vuln_get.fix_status= '2'
                vuln_get.task_id= task
                vuln_get.save()