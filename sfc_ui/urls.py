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
from rest_framework.urlpatterns import format_suffix_patterns

from sfc import views
from vim.models import vim
from vim.serializers import vim_Serializer
import vim.views as openstack_views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups',views.GroupViewSet)
router.register(r'service_function',views.service_function_ViewSet)
router.register(r'service_function_forwarder',views.service_function_forwarder_ViewSet)
router.register(r'service_function_chain',views.service_function_chain_ViewSet)
router.register(r'data_plane_locator',views.data_plane_locator_ViewSet)
router.register(r'service_function_locator',views.service_function_locator_ViewSet)
router.register(r'rendered_service_path',views.rendered_service_path_ViewSet)
router.register(r'rendered_service_path_hop_locator',views.rendered_service_path_hop_locator_ViewSet)
router.register(r'vim', openstack_views.vim_ViewSet)
router.register(r'port', openstack_views.port_ViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^vims/$', openstack_views.vim_List.as_view()),
#     url(r'^vims/(?P<pk>[0-9]+)/$', openstack_views.vim_Detail.as_view()),
]
#urlpatterns = format_suffix_patterns(urlpatterns)