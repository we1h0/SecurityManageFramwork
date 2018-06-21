#coding:utf-8
'''
Created on 2018年5月25日

@author: yuguanc
'''

from django.urls import path
from TaskManage.views import views,Scantasks

urlpatterns = [
    path('user/',views.TaskView,name='taskview'),
    path('user/list/',views.tasktablelist,name='tasklist'),
    path('user/nessus/scan/',Scantasks.ScanAll,name='scantask'),
    path('user/details/<str:task_id>/',views.taskdetails,name='taskdetails'),
    
    path('user/scantaskchoice/<str:action>/',Scantasks.scan_task,name='taskscanchoice'),
    
    path('user/scan/action/<str:task_id>/<str:action>/',views.task_action,name='taskaction'),
    path('user/task/action/<str:task_id>/<str:action>/',views.taskrequestaction,name='taskrequestaction'),
    
    path('manage/sync/',views.TaskSync,name='tasksync'),
    
    path('request/',views.TaskRequestView,name='taskrequestview'),
    path('request/list/',views.taskrequesttablelist,name='taskrequestlist'),
]