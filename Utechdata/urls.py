"""Dmitry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from udata import urls as data_urls
from udata.views import Dashviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='Utechdata/layout.html'), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/dashboard/', Dashviews.DashboardChartsView.as_view(), name='profile'),
    url(r'^accounts/personal_info/', TemplateView.as_view(template_name='Utechdata/dashboard-personal-info.html'),
        name='personal-info'),
    path('data/', include(data_urls, namespace='udata'), ),
    url('avatar/', include('avatar.urls')),
]
