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

from django.conf.urls import url, include
from rest_framework import routers

import sdn_controllers.views as sdn_controller_views
import sdn_switch.views as sdn_switch_views
from sfc import views
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
router.register(r'vim', openstack_views.VIMViewSet)
router.register(r'port', openstack_views.PortViewSet)
router.register(r'hypervisor', openstack_views.HypervisorViewSet)
router.register(r'network', openstack_views.NetworkViewSet)
router.register(r'server', openstack_views.ServerViewSet)
router.register(r'interface', openstack_views.InterfaceViewSet)
router.register(r'host', sdn_switch_views.HostViewSet)
router.register(r'openvswitch', sdn_switch_views.OpenvSwitchViewSet)
router.register(r'ovs_port', sdn_switch_views.OVSPortViewSet)
router.register(r'ovs_interface', sdn_switch_views.OVSInterfaceViewSet)
router.register(r'ovs_bridge', sdn_switch_views.OVSBridgeViewSet)
router.register(r'sdn_controller', sdn_controller_views.SDNControllerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
#urlpatterns = format_suffix_patterns(urlpatterns)