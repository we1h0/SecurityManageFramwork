#coding:utf-8
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import hashlib 
from django.contrib.auth.hashers import make_password 
# Create your views here.

#该段代码用来分页
def paging(deploy_list,limit,offset):
    
    paginator = Paginator(deploy_list, limit)
    
    try:
        deploy_list = paginator.page(offset)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        deploy_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        deploy_list = paginator.page(paginator.num_pages)
    return deploy_list



def strtopsd(string):
    hash_res = hashlib.md5()
    hash_res.update(make_password(string).encode('utf-8'))
    urlarg = hash_res.hexdigest()
    return urlarg