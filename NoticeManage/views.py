#coding:utf-8

from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
from . import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from SeMFSetting.views import paging
import json
from django.utils.html import escape
# Create your views here.

@login_required
def notice_read(request,notice_id):
    user = request.user
    
    notice = get_object_or_404(models.Notice,notice_user =user ,id =notice_id)
    notice.notice_status = True
    notice.save()
    return HttpResponseRedirect(notice.notice_url)



@login_required
def notice_count(request):
    user = request.user
    notice_count = user.notice_for_user.filter(notice_status = False).count()
    return JsonResponse({'notice_count':notice_count})



@login_required
@csrf_protect
def notice_readall(request):
    user = request.user
    error = '操作成功'
    action = request.POST.get('action')
    if action =='readall':
        notice_list = user.notice_for_user.filter(notice_status = False)
        for notice_get in notice_list:
            notice_get.notice_status = True
            notice_get.save()
    else:
        error = '参数错误'
    return JsonResponse({'error':error})



@login_required
@csrf_protect
def notice_action(request):
    user = request.user
    error = '操作成功'
    notice_id_list = request.POST.get('notice_id_list')
    notice_id_list=json.loads(notice_id_list)
    action = request.POST.get('action')
    #notice_id_list = ast.literal_eval(notice_id_list)
    for notice_id in notice_id_list:
        notice_get = get_object_or_404(models.Notice,notice_user =user ,id =notice_id )
        if action =='delete':
            notice_get.delete()
        elif action =='read':
            notice_get.notice_status = True
            notice_get.save()
        elif action =='unread':
            notice_get.notice_status = False
            notice_get.save()
        else:
            error= '参数错误'
    return JsonResponse({'error':error})
    
    



@login_required
@csrf_protect
def notice_table_list(request):
    user = request.user
    resultdict={}
    
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    notice_type=request.POST.get('notice_type')
    if not notice_type:
        notice_type = ''
    notice_status=request.POST.get('notice_status')
    if not notice_status:
        notice_status = ['True','False']
    else:
        notice_status = [notice_status]
    
    notice_list = models.Notice.objects.filter(notice_user = user,notice_status__in = notice_status,notice_type__icontains=notice_type).order_by('-notice_time')
    total = notice_list.count()
    notice_list = paging(notice_list,rows,page)
    data = []
    for notice in notice_list:
        dic={}
        dic['id'] =escape( notice.id)
        dic['notice_title'] =escape( notice.notice_title)
        dic['notice_body'] =escape( notice.notice_body)
        if notice.notice_status:
            dic['notice_status'] =escape( '已读')
        else:
            dic['notice_status'] =escape( '未读')
        dic['notice_time'] =escape( notice.notice_time)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="用户申请列表"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)
        


@login_required
def notice_view(request):
    return render(request,'NoticeManage/noticelist.html')



def notice_add(user,data):
    '''           
                这里的 data 为数据字典，内容包括
    {
        'notice_title':'***',
        'notice_body':'***',
        'notice_url':'***',
        'notice_type':'***'
    }
    '''
    notice_title = data.get('notice_title')
    notice_body = data.get('notice_body')
    notice_type = data.get('notice_type')
    notice_url = data.get('notice_url')
    
    notice_body = notice_body
    
    res = models.Notice.objects.get_or_create(
        notice_title=notice_title,
        notice_body=notice_body,
        notice_type=notice_type,
        notice_url=notice_url,
        notice_user=user,
        )
    if res[1]:
        return False
    else:
        res[0].notice_status=False
        res[0].save()
        return True
    