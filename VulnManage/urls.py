#coding:utf-8
'''
Created on 2018年5月14日

@author: yuguanc
'''
from django.urls import path
from .views import views,cnvdviews

urlpatterns = [
    path('user/',views.vulnview,name='vulnview'),
    path('user/list/',views.vulntablelist,name='vulnlist'),
    path('user/listfix/',views.vulnfixlist,name='vulnlistfix'),
    path('user/fix/<str:vuln_id>/',views.vuln_change_status,name='vulnfix'),
    path('user/details/<str:vuln_id>/',views.vulndetails,name='vulndetails'),
    
    
    path('cnvd/',cnvdviews.cnvdvuln_view,name='cnvdvulnview'),
    path('cnvd/list/',cnvdviews.cnvdvulntablelist,name='cnvdvulnlist'),
    path('cnvd/update/<str:cnvdvuln_id>',cnvdviews.cnvdvuln_update,name='cnvdvulnupdate'),
    path('cnvd/details/<str:cnvdvuln_id>',cnvdviews.cnvdvulndetails,name='cnvdvulndetails'),
    path('cnvd/vulnrenew/', cnvdviews.renew, name='cnvdvulnrenew'),
    
    path('manage/create/<str:asset_id>/',views.vulncreate,name='vulncreate'),
    path('manage/update/<str:vuln_id>/',views.vuln_update,name='vulnupdate'),
]