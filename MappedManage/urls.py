#coding:utf-8
'''
Created on 2018年5月23日

@author: yuguanc
'''


from django.urls import path
from . import views

urlpatterns = [
    path('',views.Mappedview,name='mappedview'),
    path('list/',views.MappedTableList,name='mappedlist'),
    path('create/',views.MappedCreate,name='mappedcreate'),
    path('update/<str:mapped_id>/',views.Mappedupdate,name='mappedupdate'),
    path('details/<str:mapped_id>/',views.Mappeddetails,name='mappeddetails'),
]