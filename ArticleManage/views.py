#coding:utf-8

# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from . import models,forms
from SeMFSetting.views import paging
from django.http import JsonResponse
from .Functions.uploadimgs import image_upload
from NoticeManage.views import notice_add
from django.contrib.auth.models import User
import time
import uuid
from django.utils.html import escape

ARTICLE_STATUS={
    '0':'新建',
    '1':'发布',
    '2':'撤回'
    }

@login_required
def articlerevoke(request,article_id):
    user = request.user
    error = ''
    if user.is_superuser:
        article = get_object_or_404(models.Article,article_id=article_id)
        article.article_status = '2'
        article.save()
        error = '撤回成功'
    else:
        error = '权限错误'
    return JsonResponse({'error':error})


@login_required
def articlepublic(request,article_id):
    user = request.user
    error = ''
    if user.is_superuser:
        article = get_object_or_404(models.Article,article_id=article_id)
        article.article_status = '1'
        if article.article_type.parent:
            if article.article_type.parent.article_type_name == '通告':
                data_manage={
                      'notice_title':'系统通告',
                      'notice_body': '系统发布新通告:'+article.article_type.article_type_name+'--'+article.article_name+ '，请进行查看',
                      'notice_url':'/article/user/details/'+article_id+'/',
                      'notice_type':'inform',
                      }
                user_manage_list = User.objects.all()
                for user_manage in user_manage_list:
                    notice_add(user_manage,data_manage)
            else:
                data_manage={
                      'notice_title':'知识库更新通知',
                      'notice_body':user.username +'已更新知识库,更新id为'+article_id,
                      'notice_url':'/article/user/details/'+article_id+'/',
                      'notice_type':'notice',
                      }
                user_manage_list = User.objects.filter(is_superuser=True)
                for user_manage in user_manage_list:
                    notice_add(user_manage,data_manage)
        article.save()
        error = '发布成功'
    else:
        error = '权限错误'
    return JsonResponse({'error':error})


@login_required
def articledelete(request,article_id):
    user = request.user
    error = ''
    if user.is_superuser:
        article = get_object_or_404(models.Article,article_id=article_id)
        article.delete()
        error = '删除成功'
    else:
        error = '权限错误'
    return JsonResponse({'error':error})
    


@login_required
def articledetails(request,article_id):
    user = request.user
    if user.is_superuser:
        article = get_object_or_404(models.Article,article_id=article_id)
    else:
        article = get_object_or_404(models.Article,article_status='1',article_id=article_id)
    
    return render(request, 'ArticleManage/articledetails.html', {'article': article})



@login_required
@csrf_protect
def articleupdate(request,article_id):
    user = request.user
    error = ''
    if user.is_superuser:
        article = get_object_or_404(models.Article,article_id=article_id)
        if request.method == 'POST':
            form = forms.Article_edit_form(request.POST,request.FILES,instance=article)
            if form.is_valid():
                form.save()
                error = '修改成功'
            else:
                error = '请检查输入'
        else:
            form = forms.Article_edit_form(instance=article)
        return render(request,'formupdate.html',{'form':form,'post_url':'articleupdate','argu':article_id,'error':error})
    else:
        error = '权限错误'
    return render(request,'error.html',{'error':error})




@login_required
@csrf_protect
def articlecreate(request):
    user = request.user
    error = ''
    if user.is_superuser:
        if request.method == 'POST':
            form = forms.Article_edit_form(request.POST,request.FILES)
            if form.is_valid():
                try:
                    num_id =models.Article.objects.latest('id').id
                except:
                    num_id = 0
                num_id += 1
                article_type = form.cleaned_data['article_type']
                type_id = article_type.id
                article_id = str(type_id) + time.strftime('%Y%m%d',time.localtime(time.time())) + str(num_id)
                article_name = form.cleaned_data['article_name']
                article_type = form.cleaned_data['article_type']
                article_body = form.cleaned_data['article_body']
                file = form.cleaned_data['file']
                if file:
                    file_suffix=file.name.split(".")[-1]
                    file_name=str(uuid.uuid1())+"."+file_suffix
                    file.name = file_name
                models.Article.objects.get_or_create(
                    article_id=article_id,
                    article_name=article_name,
                    article_type=article_type,
                    article_body=article_body,
                    article_user = user,
                    file=file,
                    )
                error = '创建成功'
        else:
            form = forms.Article_edit_form()
        return render(request,'formedit.html',{'form':form,'post_url':'articlecreate','error':error})
    else:
        error = '权限错误'
    return render(request,'error.html',{'error':error})



@login_required
def vulnview(request):
    articletype = models.ArticleType.objects.filter(parent__isnull=False)
    return render(request,'ArticleManage/articlelist.html',{'articletype':articletype})



@login_required
@csrf_protect
def articleablelist(request):
    user = request.user
    resultdict={}
    page = request.POST.get('page')
    rows = request.POST.get('limit')
    
    name = request.POST.get('name')
    if  not name:
        name=''
        
    artuicletype = request.POST.get('type')
    if not artuicletype:
        type_get = models.ArticleType.objects.filter(parent__isnull=False)
    else:
        type_get = models.ArticleType.objects.filter(id =artuicletype )
    
    status = request.POST.get('status')
    if  not status:
        status=''

    if user.is_superuser:
        article_list = models.Article.objects.filter(
            article_name__icontains = name,
            article_type__in = type_get,
            article_status__icontains = status
            ).order_by('article_status','-article_updatetime','-id')
    else:
        article_list = models.Article.objects.filter(
            article_status='1',
            article_name__icontains = name,
            article_type__in = type_get,
            article_status__icontains = status
            ).order_by('-article_updatetime')
    
    total = article_list.count()
    article_list = paging(article_list,rows,page)
    data = []
    for article_item in article_list:
        dic={}
        dic['article_id'] = escape(article_item.article_id)
        dic['article_name'] = escape(article_item.article_name)
        dic['article_type'] = escape(article_item.article_type.article_type_name)
        dic['article_updatetime'] = escape(article_item.article_updatetime)
        dic['article_status'] = escape(ARTICLE_STATUS[article_item.article_status])
        dic['article_user'] = escape(article_item.article_user.username)
        data.append(dic)
    resultdict['code']=0
    resultdict['msg']="知识共享"
    resultdict['count']=total
    resultdict['data']=data
    return JsonResponse(resultdict)


@csrf_exempt
@login_required
def upload_image(request):
    user = request.user
    dir_name='imgs'
    result = {
        "code": 0 
        ,"msg": ""
        ,"data": {
            "src": ""
            ,"title": "" 
          }
        }
    if user.is_superuser:
        files = request.FILES.get("file", None)
        if files:
            url =image_upload(files, dir_name)
            if url:
                result['msg'] = '上传成功'
                result['data']['src'] = url
            else:
                result['code'] = 1
                result['msg'] = '上传失败'
        else:
            result['code'] = 1
            result['msg'] = '未发现文件'
        
    else:
        result['code'] = 1
        result['msg'] = '权限错误'
    return JsonResponse(result)
    

