"""sfc_ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import UserList
from django.conf.urls import url, include, patterns
from django.contrib import admin
from rest_framework import routers

from vim import views


# router = routers.DefaultRouter()
# router.register(r'vim', views.vim_ViewSet.as_view())
# 
# urlpatterns = [
#     url(r'^', include(router.urls))
# ]
