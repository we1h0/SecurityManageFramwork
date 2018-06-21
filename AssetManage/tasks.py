#coding:utf-8
'''
Created on 2018年5月24日

@author: yuguanc
'''

from __future__ import absolute_import
from celery import shared_task
import time
from SeMFSetting.Functions import nmap
from AssetManage import models
from django.contrib.auth.models import User
from NoticeManage.views import notice_add

from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
from SeMFSetting.Functions.checkip import checkip

@shared_task
def asset_user_save(user_email,asset_id_list):
    user = User.objects.filter(email = user_email).first()
    for item in asset_id_list:
        asset_id=item
        asset = models.Asset.objects.filter(asset_id=asset_id).first()
        asset.asset_user.add(user)
        asset.save()
    return True




@shared_task
def asset_port(user_id,asset_id_list):
    user = User.objects.filter(id = user_id).first()
    for item in asset_id_list:
        asset_id=item
        asset = models.Asset.objects.filter(asset_id=asset_id).first()
        if asset:
            ip = asset.asset_key
            if checkip(ip):
                port_list =nmap.nmap_host_all(ip)
                if port_list!=0:
                    for port_info in port_list.keys():
                        port = port_info
                        name = port_list[port_info].get('name')
                        product = port_list[port_info].get('product')
                        version =  port_list[port_info].get('version')
                        port_get = models.Port_Info.objects.get_or_create(
                            port=port,
                            asset = asset,
                            )
                        if port_get[1]:
                            port = port_get[0]
                            port.product=product
                            port.name = name
                            port.version=version
                            port.save()
                    data_manage={
                                  'notice_title':'资产发现通知',
                                  'notice_body':'您对'+ ip +'的端口发现任务完成',
                                  'notice_url':'/asset/user/',
                                  'notice_type':'notice',
                                  }
                    notice_add(user,data_manage)
                else:
                    data_manage={
                                  'notice_title':'资产发现通知',
                                  'notice_body':'您对'+ ip +'的端口发现任务完成,该主机未开放端口或网络不可达',
                                  'notice_url':'/asset/user/',
                                  'notice_type':'notice',
                                  }
                    notice_add(user,data_manage)
            else:
                return False
        else:
            return False
    
    return True



@shared_task
def asset_descover(user_id,asset_id_list):
    
    user = User.objects.filter(id = user_id).first()
    data_manage={
                      'notice_title':'资产发现通知',
                      'notice_body':'您的资产发现任务已开始，请勿重复提交',
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
    notice_add(user,data_manage)
    for item in asset_id_list:
        asset_id=item
        asset_type = models.AssetType.objects.filter(name = 'IP地址段').first()
        segment_asset = models.Asset.objects.filter(asset_id = asset_id,asset_type=asset_type).first()
        if segment_asset:
            segment = segment_asset.asset_key
            host_list = nmap.nmap_alive_lists(segment)
            if host_list == None:
                data_manage={
                          'notice_title':'资产发现通知',
                          'notice_body':'针对网段'+segment+'的资产扫描任务已完成，网络不可达或无存活主机',
                          'notice_url':'/asset/user/',
                          'notice_type':'notice',
                          }
                notice_add(user,data_manage)
            else:
                asset_type = models.AssetType.objects.filter(name = '服务器').first()
                for host in host_list:
                    asset_get = models.Asset.objects.get_or_create(asset_key=host)
                    if asset_get[1]:
                        asset_host=asset_get[0]
                        try:
                            num_id =models.Asset.objects.latest('id').id
                        except:
                            num_id = 0
                        num_id += 1
                        asset_id = '01' + time.strftime('%Y%m%d',time.localtime(time.time()))+str(num_id)
                        asset_name = segment_asset.asset_name + '-服务器-' + asset_id
                        asset_host.asset_id=asset_id
                        asset_host.asset_name=asset_name
                        asset_host.asset_area = segment_asset.asset_area
                        asset_host.asset_type = asset_type
                        asset_host.asset_connect.add(segment_asset)
                        asset_host.save()
                segment_asset.asset_check=True
                segment_asset.save()
        else:
            return False
    data_manage={
                  'notice_title':'资产发现通知',
                  'notice_body':'您的资产发现任务已完成，请注意查看',
                  'notice_url':'/asset/user/',
                  'notice_type':'notice',
                  }
    notice_add(user,data_manage)
    return True
            
    