#coding:utf-8
'''
Created on 2018年5月21日

@author: yuguanc
'''
from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .. import models,forms
from SeMFSetting.views import paging
from django.http import JsonResponse
from django.db.models import Q
from ..tasks import parse_cnvdxml
from SeMF.settings import MEDIA_ROOT
import os
from django.utils.html import escape


@login_required
@csrf_protect
def renew(request):
    user = request.user
    error = ''
    if user.is_superuser:
        if request.method =='POST':
            form = forms.Cnvd_file_form(request.POST,request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                if file.name.lower().endswith('.xml'):
                    if file.content_type == 'text/xml':
                        file_list = models.Cnvdfiles.objects.get_or_create(
                                                                    file=file,
                                                                    title = file.name,
                                                                    )
                        for file in file_list:
                            filepath = os.path.join(MEDIA_ROOT,'cnvd',file.title)
                            parse_cnvdxml.delay(filepath)
                            break
                        error = '更新成功'
                    else:
                        error = '文件错误'
                else:
                    error = '文件错误'
            else:
                error = '文件错误'
        else:
            form = forms.Cnvd_file_form()
            return render(request,'formedit.html',{'form':form,'post_url':'cnvdvulnrenew','title':'同步漏洞库'})
    else:
        error = '权限不足'
    return render(request,'error.html',{'error':error})


@login_required
def cnvdvulndetails(request,cnvdvuln_id):
    vuln = get_object_or_404(models.Vulnerability,id=cnvdvuln_id)
    return render(request,'VulnManage/cnvdvulndetails.html',{'vuln':vuln})


@login_required
@csrf_protect
def cnvdvuln_update(request,cnvdvuln_id):
    user = request.user
    error = ''
    if user.is_superuser:
        cnvd_vuln= get_object_or_404(models.Vulnerability,id = cnvdvuln_id)
        if request.method == 'POST':
            form = forms.Cnvd_vuln_form(request.POST,instance =cnvd_vuln)
            if form.is_valid():
                form.save()
                error = '修改成功'
        else:
            form = forms.Cnvd_vuln_form(instance =cnvd_vuln)
        return render(request,'formupdate.html',{'form':form,'post_url':'cnvdvulnupdate','argu':cnvdvuln_id,'error':error})
    else:
        error = '权限错误'
        return render(request,'error.html',{'error':error})
    


@login_required
def cnvdvuln_view(request):
    return render(request,'VulnManage/cnvdvulnlist.html')


@login_required
@csrf_protect
def cnvdvulntablelist(request):
    resultdict={}
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    name = request.POST.get('name')
    if  not name:
        name=''
    
    leave = request.POST.get('leave')
    if  not leave:
        leave=''
    
    
    vuln_list = models.Vulnerability.objects.filter(
        Q(cve_id__icontains = name)|
        Q(cnvd_id__icontains = name) | Q(cve_name__icontains = name)
        ).filter(leave__icontains = leave).order_by('-update_data')
        
    total = vuln_list.count()
    vuln_list = paging(vuln_list,rows,page)
    data = []
    for vuln_item in vuln_list:
        dic={}
        dic['id'] =escape( vuln_item.id)
        dic['cve_id'] =escape( vuln_item.cve_id)
        dic['cnvd_id'] =escape( vuln_item.cnvd_id)
        dic['cve_name'] =escape( vuln_item.cve_name)
        dic['leave'] =escape( vuln_item.leave)
        dic['update_data'] =escape( vuln_item.update_data)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="漏洞列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)