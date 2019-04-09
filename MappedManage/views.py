#coding:utf-8

'''
Created on 2018年5月23日

@author: yuguanc
'''
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from SeMFSetting.views import paging
from django.http import JsonResponse
from . import models,forms
from django.db.models import Q
from django.utils.html import escape


@login_required
@csrf_protect
def Mappeddetails(request,mapped_id):
    mapped = get_object_or_404(models.Mapped,id = mapped_id)
    return render(request,'MappedManage/mappeddetails.html',{'mapped':mapped})




@login_required
@csrf_protect
def Mappedupdate(request,mapped_id):
    error = ''
    mapped = get_object_or_404(models.Mapped,id = mapped_id)
    if request.method == 'POST':
        form = forms.Mapped_update_form(request.POST,instance=mapped)
        if form.is_valid():
            form.save()
            error = '保存成功'
        else:
            error = '保存失败'
    else:
        form = forms.Mapped_update_form(instance=mapped)
    return render(request,'formupdate.html',{'form':form,'post_url':'mappedupdate','argu':mapped_id,'error':error})
        





@login_required
@csrf_protect
def MappedCreate(request):
    error = ''
    if request.method == 'POST':
        form = forms.Mapped_edit_form(request.POST)
        if form.is_valid():
            LANip = form.cleaned_data['LANip']
            LANip = get_object_or_404(models.Asset,asset_key=LANip)
            
            LANPort = form.cleaned_data['LANPort']
            try:
                LANPort = int(LANPort)
            except:
                error = '请检查输入'
            LANPort = models.Port_Info.objects.get_or_create(asset=LANip,port=LANPort)
            LANPort = LANPort[0]
            
            WANip = form.cleaned_data['WANip']
            WANip = get_object_or_404(models.Asset,asset_key=WANip)
            
            WANPort = form.cleaned_data['WANPort']
            try:
                WANPort = int(WANPort)
            except:
                error = '请检查输入'
            WANPort = models.Port_Info.objects.get_or_create(asset=WANip,port=WANPort)
            WANPort = WANPort[0]
            
            if error == '':
                Domain = form.cleaned_data['Domain']
                start_time = form.cleaned_data['start_time']
                end_time = form.cleaned_data['end_time']
                request_email = form.cleaned_data['request_email']
                action_email = form.cleaned_data['action_email']
                request_order = form.cleaned_data['request_order']
                request_user = form.cleaned_data['request_user']
                request_user_num = form.cleaned_data['request_user_num']
                request_user_department = form.cleaned_data['request_user_department']
                telephone = form.cleaned_data['telephone']
                Mapped_description = form.cleaned_data['Mapped_description']
                
                mapped_get = models.Mapped.objects.get_or_create(
                        LANip=LANip,
                        LANPort=LANPort,
                        WANip=WANip,
                        WANPort=WANPort,
                        Domain=Domain,
                        start_time=start_time,
                        end_time=end_time,
                        )
                mapped_get = mapped_get[0]
                mapped_get.request_email=request_email
                mapped_get.action_email=action_email
                mapped_get.request_order=request_order
                mapped_get.request_user=request_user
                mapped_get.request_user_num=request_user_num
                mapped_get.request_user_department=request_user_department
                mapped_get.telephone=telephone
                mapped_get.Mapped_description=Mapped_description
                mapped_get.save()
                WANip.asset_connect.add(LANip)
                WANip.save()
                error = '保存成功'
        else:
            error = '请检查输入'
    else:
        form = forms.Mapped_edit_form()
    return render(request,'formedit.html',{'form':form,'post_url':'mappedcreate','error':error})



@login_required
def Mappedview(request):
    return render(request,'MappedManage/mappedview.html')

@login_required
@csrf_protect
def MappedTableList(request):
    #user= request.user
    resultdict={}
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    name = request.POST.get('name')
    if  not name:
        name=''
        
    status = request.POST.get('status')
    if not status:
        status= ['True','False']
    else:
        status=[status]
    
    
    
    mappedlist = models.Mapped.objects.filter(
        Q(LANip__asset_key__icontains = name) | Q(WANip__asset_key__icontains = name)
        | Q(request_user_num__icontains = name) | Q(request_email__icontains = name)
        ).filter(mapped_status__in = status).order_by('mapped_updatetime')
    total = mappedlist.count()
    mappedlist = paging(mappedlist,rows,page)
    data = []
    for item in mappedlist:
        dic={}
        dic['id'] =escape( item.id)
        dic['LANip'] =escape( item.LANip.asset_key)
        dic['LANip_id'] =escape( item.LANip.asset_id)
        dic['LANPort'] =escape( item.LANPort.port)
        dic['WANip'] =escape( item.WANip.asset_key)
        dic['WANip_id'] =escape( item.WANip.asset_id)
        dic['WANPort'] =escape( item.WANPort.port)
        dic['Domain'] =escape( item.Domain)
        if item.mapped_status:
            dic['mapped_status'] =escape( '使用中')
        else:
            dic['mapped_status'] =escape( '已禁用')
        dic['start_time'] =escape( item.start_time)
        dic['end_time'] =escape( item.end_time)
        dic['request_email'] =escape( item.request_email)
        dic['action_email'] =escape( item.action_email)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="用户列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)