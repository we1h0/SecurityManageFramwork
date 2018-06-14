#coding:utf-8
'''
Created on 2018年5月15日

@author: yuguanc
'''

from django.urls import path
from .views import views,assetdetails,port,plugin,file,assetconnect,assetinfo,taskview,handover,csv

urlpatterns = [
    path('user/',views.assetview,name='assetview'),
    path('user/list/',views.assettablelist,name='assetlist'),
    path('user/create/',views.asset_create,name='assetcreate'),
    path('user/request/',views.asset_request,name='assetrequest'),
    path('user/delete/',views.assetdelete,name='assetdelete'),
    path('user/update/<str:asset_id>/',views.assetupdate,name='assetupdate'),
    path('user/details/<str:asset_id>/',assetdetails.assetdetailsview,name='assetdetails'),
    
    
    path('user/csv/os/',csv.create_csv_os,name='createoscsv'),
    path('user/csv/web/',csv.create_csv_web,name='createwebcsv'),
    path('user/csv/vuln/',csv.create_csv_vuln,name='createvulncsv'),
    path('user/csv/upload/',csv.file_update,name='createuploadcsv'),
    
    
    path('user/handover/',handover.asset_handover,name='assethandover'),
    
    path('handover/',handover.handoverview,name='assethandoverview'),
    path('handover/list/',handover.asset_handover_list,name='assethandoverlist'),
    path('handover/action/',handover.asset_handover_action,name='assethandoveraction'),
    
    
    
    path('user/task/',taskview.task_action,name='assettaskaction'),
    
    path('user/update/osinfo/<str:os_id>/',assetinfo.osinfpupdate,name='assetosinfoupdate'),
    path('user/update/internetinfo/<str:internet_id>/',assetinfo.internetinfpupdate,name='assetinternetinfoupdate'),
    
    
    path('user/port/<str:asset_id>/',assetdetails.asset_ports,name='porttable'),
    path('user/create/port/<str:asset_id>/',port.portcreate,name='portcreate'),
    path('user/update/port/<str:port_id>/',port.portupdate,name='portupdate'),
    path('user/delete/port/<str:port_id>/',port.portdelete,name='portdelete'),
    
    path('user/vuln/<str:asset_id>/',assetdetails.asset_vuln,name='vulntable'),
    
    
    path('user/plugin/<str:asset_id>/',assetdetails.asset_plugin,name='plugintable'),
    path('user/create/plugin/<str:asset_id>/',plugin.plugincreate,name='plugincreate'),
    path('user/update/plugin/<str:plugin_id>/',plugin.pluginupdate,name='pluginupdate'),
    path('user/delete/plugin/<str:plugin_id>/',plugin.plugindelete,name='plugindelete'),
    
    path('user/file/<str:asset_id>/',assetdetails.asset_file,name='filetable'),
    path('user/create/file/<str:asset_id>/',file.filecreate,name='filecreate'),
    path('user/update/file/<str:file_id>/',file.fileupdate,name='fileupdate'),
    path('user/delete/file/<str:file_id>/',file.filedelete,name='filedelete'),
    
    
    path('user/assetconnect/<str:asset_id>/',assetdetails.asset_asset,name='assetconnecttable'),
    path('user/create/assetconnect/<str:asset_id>/',assetconnect.assetconnectcreate,name='assetconnectcreate'),
    path('user/delete/assetconnect/<str:asset_id>/<str:assetconnect_id>/',assetconnect.assetconnectdelete,name='assetconnectdelete'),
    
    path('request/',views.assetrequestview,name='assetmanagerequest'),
    path('request/list/',views.assetreqeustlist,name='assetrequestlist'),
    path('request/action/',views.assetrequestaction,name='assetrequestaction'),
    path('request/listaction/',views.asset_request_list_action,name='assetrequestlistaction'),
    
    
    path('manage/',taskview.assetuser_action,name='assetuseraction'),
    path('manage/<str:assetuser_id>/',taskview.assetuser,name='assetuserdo'),
    
]