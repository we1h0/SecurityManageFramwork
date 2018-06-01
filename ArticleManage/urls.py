#coding:utf-8
'''
Created on 2018年5月22日

@author: yuguanc
'''
from django.urls import path

from . import views


urlpatterns = [
    path('user/', views.vulnview, name='articleview'),
    path('user/list/', views.articleablelist, name='articlelist'),
    path('user/details/<str:article_id>/', views.articledetails, name='articledetails'),
    
    path('manage/create/', views.articlecreate, name='articlecreate'),
    path('manage/update/<str:article_id>/', views.articleupdate, name='articleupdate'),
    path('manage/delete/<str:article_id>/', views.articledelete, name='articledelete'),
    path('manage/revoke/<str:article_id>/', views.articlerevoke, name='articlerevoke'),
    path('manage/public/<str:article_id>/', views.articlepublic, name='articlepublic'),
    
    path('manage/imgupload/', views.upload_image, name='imgupload'),
]
