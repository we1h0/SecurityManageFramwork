#coding:utf-8
'''
Created on 2018年5月14日

@author: yuguanc
'''
from django.urls import path
from . import views

urlpatterns = [
    path('',views.chartview,name='chartview'),
    
    path('assettype/',views.getassettype,name='chartassettype'),
    path('vulnleave/',views.getvulnleave,name='chartvulnleave'),
    path('vulnstatus/',views.getvulnstatus,name='chartvulnstatus'),
     path('vulnname/',views.getvulnname,name='chartvulnname'),
    
    path('getdatemonth/',views.getdatemonth,name='chartgetdatemonth'),
    
]