#coding:utf-8
'''
Created on 2018年6月8日

@author: yuguanc
'''
from django.shortcuts import HttpResponse,render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import csv,codecs,uuid,os,time
from django.contrib.auth.models import User
from AssetManage.models import Asset,AssetType,OS_Info,Internet_Info
from VulnManage.models import Vulnerability_scan
from SeMFSetting import forms
from SeMF.settings import MEDIA_ROOT
from SeMFSetting.models import files
from NoticeManage.views import notice_add

def vuln_upload(user_id,file_psth,name):
    user = User.objects.filter(id = user_id).first()
    with open(file_psth,'rt') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            if i >=1:
                asset_key = row[0]
                vuln_name = row[1]
                asset = Asset.objects.filter(asset_key=asset_key).first()
                if asset:
                    cve_name = row[2]
                    leave=row[3]
                    scopen=row[4]
                    introduce=row[5]
                    vuln_info=row[6]
                    fix=row[7]
                    try:
                        num = Vulnerability_scan.objects.latest('id').id
                    except Exception:
                        num = 0
                    num =num+1
                    vuln_id = str(asset.asset_type.id) + time.strftime('%Y%m%d',time.localtime(time.time())) + str(num)
                    try:
                        res=Vulnerability_scan.objects.get_or_create(
                                                                     vuln_name=vuln_name,
                                                                     cve_name=cve_name,
                                                                     leave=leave,
                                                                     introduce=introduce,
                                                                     vuln_info=vuln_info,
                                                                     scopen=scopen,
                                                                     fix=fix,
                                                                     vuln_asset = asset,
                                                                     )
                        vuln = res[0]
                        if vuln.vuln_id == vuln_id:
                            if vuln.fix_status == '1':
                                vuln.fix_status= '3'
                        else:
                            vuln.vuln_id = vuln_id
                            if leave == '0':
                                vuln.fix_status= '0'
                            vuln.fix_status= '2'
                        vuln.save()
                    except:
                        data_manage={
                          'notice_title':'漏洞导入通知',
                          'notice_body':'您对'+asset_key+'的'+ vuln_name +'的漏洞导入出现问题，可能原因为漏洞格式不正确',
                          'notice_url':'/asset/user/',
                          'notice_type':'notice',
                          }
                        notice_add(user,data_manage)
                else:
                    data_manage={
                      'notice_title':'漏洞导入通知',
                      'notice_body':'您对'+asset_key+'的'+ vuln_name +'的漏洞导入出现问题，可能原因为资产不存在',
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
                    notice_add(user,data_manage)
        data_manage={
                      'notice_title':'漏洞导入通知',
                      'notice_body':'您对'+ name +'的漏洞导入任务已完成',
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
        notice_add(user,data_manage)
                




def os_asset_upload(user_id,file_psth,name):
    user = User.objects.filter(id = user_id).first()
    with open(file_psth,'rt') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            if i >=1:
                asset_name = row[0]
                asset_out_id=row[1]
                asset_type = row[2]
                asset_key=row[3]
                os = row[4]
                cpu_model = row[5]
                cpu_num = row[6]
                memory = row[7]
                disk = row[8]
                vendor = row[9]
                sn = row[10]
                user_email=row[11]
                asset_type = AssetType.objects.filter(name=asset_type).first()
                if asset_type:
                    res = Asset.objects.get_or_create(asset_key=asset_key)
                    asset=res[0]
                    if res[1]:
                        try:
                            num_id =Asset.objects.latest('id').id
                        except:
                            num_id = 0
                        num_id += 1
                        asset_id = '01' + time.strftime('%Y%m%d',time.localtime(time.time()))+str(num_id)
                        asset.asset_id = asset_id
                    asset.asset_name=asset_name
                    asset.asset_out_id=asset_out_id
                    asset.asset_type=asset_type
                    asset.user_email=user_email
                    asset.save()
                    try:
                        os_info = asset.os_for_asset
                    except:
                        OS_Info.objects.get_or_create(asset=asset)
                        os_info = asset.os_for_asset
                    os_info.os=os
                    os_info.cpu_model=cpu_model
                    os_info.cpu_num=cpu_num
                    os_info.memory=memory
                    os_info.disk=disk
                    os_info.vendor=vendor
                    os_info.sn=sn
                    os_info.save()
                else:
                    data_manage={
                      'notice_title':'资产导入通知',
                      'notice_body':'您对'+ asset_key +'的信息导入出现问题，可能原因是资产类型错误，请检查',
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
                    notice_add(user,data_manage)
        data_manage={
                      'notice_title':'资产发现通知',
                      'notice_body':'您对'+ name +'的资产导入任务已完成',
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
        notice_add(user,data_manage)
        
            
def web_asset_upload(user_id,file_psth,name):
    user = User.objects.filter(id = user_id).first()
    with open(file_psth,'rt') as f:
        reader = csv.reader(f)
        for i,row in enumerate(reader):
            if i >=1:
                asset_name = row[0]
                asset_out_id=row[1]
                asset_type = row[2]
                asset_key=row[3]
                user_email=row[4]
                middleware = row[5]
                middleware_version = row[6]
                out_key = row[7]
                language = row[8]
                language_version = row[9]
                web_framwork = row[10]
                web_framwork_version = row[11]
                
                
                asset_type = AssetType.objects.filter(name=asset_type).first()
                if asset_type:
                    res = Asset.objects.get_or_create(asset_key=asset_key)
                    asset=res[0]
                    if res[1]:
                        try:
                            num_id =Asset.objects.latest('id').id
                        except:
                            num_id = 0
                        num_id += 1
                        asset_id = '01' + time.strftime('%Y%m%d',time.localtime(time.time()))+str(num_id)
                        asset.asset_id = asset_id
                    asset.asset_name=asset_name
                    asset.asset_out_id=asset_out_id
                    asset.asset_type=asset_type
                    asset.user_email=user_email
                    asset.save()
                    try:
                        internet_info = asset.internet_for_asset
                    except:
                        internet_info = Internet_Info.objects.get_or_create(asset=asset)
                        internet_info=internet_info[0]
                    internet_info.middleware=middleware
                    internet_info.middleware_version=middleware_version
                    internet_info.out_key=out_key
                    internet_info.language=language
                    internet_info.language_version=language_version
                    internet_info.web_framwork=web_framwork
                    internet_info.web_framwork_version=web_framwork_version
                    internet_info.save()
                else:
                    data_manage={
                      'notice_title':'资产导入通知',
                      'notice_body':'您对'+ asset_key +'的信息导入出现问题，可能原因是资产类型错误，请检查',
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
                    notice_add(user,data_manage)
        data_manage={
                      'notice_title':'资产导入通知',
                      'notice_body':'您对'+ name +'的资产导入任务已完成',
                      'notice_url':'/asset/user/',
                      'notice_type':'notice',
                      }
        notice_add(user,data_manage)

@login_required
def create_csv_os(request):
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment;filename=asset_os.csv'
    
    writer = csv.writer(response)
    headers = [u"资产名称",u"资产编号",u"资产类型",u"资产标识",u'操作系统',u'CPU型号','CPU数量',u'内存大小',u'硬盘大小',u'设备厂商',u'SN号',u'使用人员']
    headers = [item for item in headers]
    writer.writerow(headers)
    
    return response

@login_required
@csrf_protect
def file_update(request):
    user = request.user
    error = ''
    if request.method == 'POST':
        form = forms.File(request.POST,request.FILES)
        if form.is_valid():
            file_type = form.cleaned_data['file_type']
            file = form.cleaned_data['file']
            name = form.cleaned_data['name']
            
            file_suffix=file.name.split(".")[-1]
            if file_suffix=='csv':
                file_name=str(uuid.uuid1())+"."+file_suffix
                file.name = file_name
                files.objects.get_or_create(
                    name=name,
                    file_type=file_type,
                    file=file,
                    action_user=user
                    )
                error = '上传成功'
                filepath = os.path.join(MEDIA_ROOT,'files',file_name)
                if file_type == '网络设备':
                    os_asset_upload(user.id,filepath,name)
                elif file_type == '业务系统':
                    web_asset_upload(user.id,filepath,name)
                elif file_type == '漏洞列表':
                    vuln_upload(user.id,filepath,name)
                else:
                    error = '请检查输入'
            else:
                error ='请检查文件是否正确'
        else:
            error = '检查输入'
    else:
        form = forms.File()
    return render(request,'formedit.html',{'form':form,'post_url':'createuploadcsv','error':error})

@login_required
def create_csv_web(request):
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment;filename=asset_web.csv'
    
    writer = csv.writer(response)
    headers = [u"资产名称",u"资产编号",u"资产类型",u"资产标识",u'管理人员',u'中间件',u'中间件版本',u'外网域名',u'开发语言',u'语言版本',u'开发框架',u'框架版本']
    headers = [item for item in headers]
    writer.writerow(headers)
    
    return response


@login_required
def create_csv_vuln(request):
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = 'attachment;filename=asset_vuln.csv'
    
    writer = csv.writer(response)
    headers = [u"资产标识",u"漏洞名称",u'CVE编号',u"危险等级0-4",u'影响范围',u"漏洞介绍",u'漏洞信息',u'修复建议']
    headers = [item for item in headers]
    writer.writerow(headers)
    
    return response