#coding:utf-8
'''
Created on 2018年5月24日

@author: yuguanc
'''



from django.shortcuts import render

def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')