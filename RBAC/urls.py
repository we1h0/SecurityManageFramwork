#coding:utf-8
'''
Created on 2018年5月10日

@author: yuguanc
'''

from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('view/', views.login, name='login'),
    path('view/regist/<str:argu>/', views.regist, name='regist'),
    path('view/resetpsd/<str:argu>/', views.resetpasswd, name='resetpsds'),
    path('user/', views.dashboard, name='dashboard'),
    path('user/main/', views.main, name='main'),
    path('user/logout/', views.logout, name='logout'),
    path('user/changepsd/', views.changepsd, name='changepsd'),
    path('user/info/', views.userinfo, name='userinfo'),
    path('user/changeinfo/', views.changeuserinfo, name='changeuserinfo'),
    
    path('manage/user/', views.userlist, name='userview'),
    path('manage/user/list/', views.userlisttable, name='userlist'),
    path('manage/user/add/', views.user_add, name='useradd'),
    path('manage/user/disactivate/', views.user_disactivate, name='userdisactivate'),
    
    path('manage/userrequest/', views.userregistlist, name='userregistview'),
    path('manage/userrequest/list/', views.userregisttable, name='userregistlist'),
    path('manage/userrequest/action/', views.userregistaction, name='userregistaction'),
    path('manage/userrequest/stop/', views.user_request_cancle, name='userregiststop'),
    
    
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)