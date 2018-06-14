#coding:utf-8
'''
Created on 2018年4月16日

@author: yuguanc
'''

from django.conf import settings
from django.shortcuts import HttpResponse, redirect,render,HttpResponseRedirect 
import re
from AssetManage.models import File

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response
    
class RbacMiddleware(MiddlewareMixin):
    """
    检查用户的url请求是否是其权限范围内
    """
    def process_request(self, request):
        request_url = request.path_info
        permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
        # 如果请求url在白名单，放行
        if request_url =='/':
            if request.user.is_authenticated:
                return HttpResponseRedirect('/user/')
            else:
                return HttpResponseRedirect('/view/')
        elif re.match('/semf/', request_url):
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    return None
                else:
                    error ='权限错误'
                    return render(request,'error.html',{'error':error})
            else:
                return HttpResponseRedirect('/view/')
        elif re.match('/uploads/imgs/', request_url):
            return None
        elif re.match('/uploads/files/', request_url):
            if request.user.is_superuser:
                return None
            else:
                error ='权限错误'
                return render(request,'error.html',{'error':error})
        elif re.match('/uploads/assetfiles/', request_url):
            url_get = File.objects.filter(asset__asset_user=request.user,file=request_url)
            if url_get:
                return None
            else:
                if request.user.is_superuser:
                    return None
                else:
                    error ='权限错误'
                    return render(request,'error.html',{'error':error})
        else:
            for url in settings.SAFE_URL:
                if re.match(url, request_url):
                    return None

        # 如果未取到permission_url, 重定向至登录；为了可移植性，将登录url写入配置
        if not permission_url:
            return redirect(settings.LOGIN_URL)

        # 循环permission_url，作为正则，匹配用户request_url
        # 正则应该进行一些限定，以处理：/user/ -- /user/add/匹配成功的情况
        flag = False
        for url in permission_url:
            url_pattern = settings.REGEX_URL.format(url=url)
            if re.match(url_pattern, request_url):
                flag = True
                break
        if flag:
            return None
        else:
            # 如果是调试模式，显示可访问url
            if settings.DEBUG:
                info ='<br/>' + ( '<br/>'.join(permission_url))
                return HttpResponse('无权限，请尝试访问以下地址：%s' %info)
            else:
                return HttpResponse('无法访问')