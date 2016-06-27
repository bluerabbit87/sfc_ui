from django.conf.urls import url, include
from rest_framework import routers

import floodlight.views as sdn_controller_views
import openvswitch.views as sdn_switch_views
from sfc import views
import openstack.views as openstack_views
import ui.views as ui_views

# router.register(r'service_function_locator',views.service_function_locator_ViewSet)
# router.register(r'rendered_service_path',views.rendered_service_path_ViewSet)
# router.register(r'rendered_service_path_hop_locator',views.rendered_service_path_hop_locator_ViewSet)

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups',views.GroupViewSet)

router.register(r'service_function',views.ServiceFunctionViewSet)
router.register(r'service_function_Groups',views.ServiceFunctionGroupsViewSet)
router.register(r'service_function_chain',views.ServiceFunctionChainViewSet)
router.register(r'flow_classifier',views.FlowClassifierViewSet)

router.register(r'openstack', openstack_views.VIMViewSet)
router.register(r'port', openstack_views.PortViewSet)
router.register(r'hypervisor', openstack_views.HypervisorViewSet)
router.register(r'network', openstack_views.NetworkViewSet)
router.register(r'server', openstack_views.ServerViewSet)
router.register(r'interface', openstack_views.InterfaceViewSet)

router.register(r'ovs', sdn_switch_views.OpenvSwitchViewSet)
router.register(r'ovs_port', sdn_switch_views.OVSPortViewSet)
router.register(r'ovs_interface', sdn_switch_views.OVSInterfaceViewSet)
router.register(r'ovs_bridge', sdn_switch_views.OVSBridgeViewSet)
router.register(r'ovs_controller', sdn_switch_views.OVSControllerViewSet)

router.register(r'floodlight', sdn_controller_views.SDNControllerViewSet)
router.register(r'openvswitch', sdn_controller_views.OpenFlowSwitchViewSet)
router.register(r'sdn_flowentry', sdn_controller_views.OpenFlowEntryViewSet)
router.register(r'sdn_port', sdn_controller_views.OpenFlowPortViewSet)
router.register(r'sdn_topology_link', sdn_controller_views.OpenFlowTopologyLinkViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^test/', ui_views.index, name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
#urlpatterns = format_suffix_patterns(urlpatterns)