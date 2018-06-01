#coding:utf-8
'''
Created on 2018年5月14日

@author: yuguanc
'''
from django.urls import path
from . import views

urlpatterns = [
    path('',views.notice_view,name='noticeview'),
    path('list/',views.notice_table_list,name='noticelist'),
    path('action/',views.notice_action,name='noticeaction'),
    path('readall/',views.notice_readall,name='noticereadall'),
    path('count/',views.notice_count,name='noticecount'),
    path('read/<str:notice_id>/',views.notice_read,name='noticeread'),
]