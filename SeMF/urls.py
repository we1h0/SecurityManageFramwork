"""SeMF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('semf/', admin.site.urls),
    path('',include('RBAC.urls')),
    path('notice/',include('NoticeManage.urls')),
    path('asset/',include('AssetManage.urls')),
    path('vuln/',include('VulnManage.urls')),
    path('chart/',include('ChartManage.urls')),
    path('article/',include('ArticleManage.urls')),
    path('mapped/',include('MappedManage.urls')),
    path('task/',include('TaskManage.urls')),
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    
handler404 = views.page_not_found
handler500 = views.page_error
handler403 = views.permission_denied