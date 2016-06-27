from django.contrib.auth.models import User, Group
import json
import pprint
import requests
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from openstack.models import Port
from openvswitch.models import OVSInterface, OVSBridge
from sfc.models import ServiceFunctionGroup, \
    ServiceFunctionChain, FlowClassifier, ServiceFunction
from sfc.serializers import GroupSerializer, \
    UserSerializer, \
    ServiceFunctionChainSerializer, ServiceFunctionSerializer, \
    ServiceFunctionGroupsSerializer, FlowClassifierSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ServiceFunctionViewSet(viewsets.ModelViewSet):
    queryset = ServiceFunction.objects.all()
    serializer_class = ServiceFunctionSerializer

class ServiceFunctionGroupsViewSet(viewsets.ModelViewSet):
    queryset = ServiceFunctionGroup.objects.all()
    serializer_class = ServiceFunctionGroupsSerializer

class ServiceFunctionChainViewSet(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
                                  
    queryset = ServiceFunctionChain.objects.all()
    serializer_class = ServiceFunctionChainSerializer
    
    def show_sfc_parameter(self,sfc_data):
        print "load_sfc_parameter"
        
        print "id: %s" % sfc_data.id
        print "name: %s" % sfc_data.name
        print "description: %s" % sfc_data.description
        print "active: %s" % sfc_data.active
        print "chain_parameters: %s" % sfc_data.chain_parameters
        
        sf_group_list =  ServiceFunctionGroup.objects.filter(service_function_chain=sfc_data.id)
        for sf_group in sf_group_list:
            print "-----Service Function Group----------"
            print "id: %s" % sf_group.id
            print "tenant_id: %s" % sf_group.tenant_id
            print "name: %s" % sf_group.name
            print "description: %s" % sf_group.description
            print "--------------------------------------"
            print ""
        
            sf_list = ServiceFunction.objects.filter(Service_function_groups=sf_group.id)
            for sf in sf_list:
                
                print "-----Service Function ----------"
                print "id: %s" % sf.id
                print "tenant_id: %s" % sf.tenant_id
                print "name: %s" % sf.name
                print "description: %s" % sf.description
                print "ingress: %s" % sf.ingress
                ingress_port = Port.objects.get(pk=sf.ingress)
                print "ingress mac address: %s" % ingress_port.mac_address
                ingress_ovs_interface = OVSInterface.objects.filter(attached_mac=ingress_port.mac_address)
                print "ingress ofport num: %s" % ingress_ovs_interface[0].ofport
                print "egress: %s" % sf.egress
                egress_port = Port.objects.get(id=sf.egress)
                print "egress mac address: %s" % egress_port.mac_address
                egress_ovs_interface = OVSInterface.objects.filter(attached_mac=egress_port.mac_address)
                print "egress ofport num: %s" % egress_ovs_interface[0].ofport
                print "service_function_parameters: %s" % sf.service_function_parameters
                print "--------------------------------"
                print ""
                
        
        flowclassifier_list = FlowClassifier.objects.filter(service_function_chain=sfc_data.id)
        print flowclassifier_list
        for flowclassifier in flowclassifier_list:
            print "id: %s" % flowclassifier.id 
            print "name: %s" % flowclassifier.name 
            print "description: %s" % flowclassifier.description 
            print "ethertype: %s" % flowclassifier.ethertype 
            print "protocol: %s" % flowclassifier.protocol 
            print "source_port_range_min: %s" % flowclassifier.source_port_range_min 
            print "source_port_range_max: %s" % flowclassifier.source_port_range_max 
            print "destination_port_range_min: %s" % flowclassifier.destination_port_range_min 
            print "destination_port_range_max: %s" % flowclassifier.destination_port_range_max 
            print "source_ip_prefix: %s" % flowclassifier.source_ip_prefix 
            print "destination_ip_prefix: %s" % flowclassifier.destination_ip_prefix 
            print "logical_source_port: %s" % flowclassifier.logical_source_port 
            logical_source_port = Port.objects.get(id=flowclassifier.logical_source_port)
            print "logical_source_port mac address: %s" % logical_source_port.mac_address
            logical_source_ovs_interface = OVSInterface.objects.filter(attached_mac=logical_source_port.mac_address)
            print "logical_source_port ofport num: %s" % logical_source_ovs_interface[0].ofport
            print "logical_destination_port: %s" % flowclassifier.logical_destination_port 
            print "l7_parameters: %s" % flowclassifier.l7_parameters 
            
            
        ovs_bridges = []
        br_ints = OVSBridge.objects.filter(name="br-int")
        for br_int in br_ints:
            print "br-ints %s" % br_int.datapath_id
            
    def load_sfc_parameter(self,sfc_data):
        print "load_sfc_parameter"
        params = {}
        params ["id"]           = sfc_data.id
        params ["name"]         = sfc_data.name
        params ["description"]  = sfc_data.description
        params ["active"]       = sfc_data.active
        params ["chain_parameters"]   = sfc_data.chain_parameters
        
        service_function_group_list  =  []
        params ["service_function_groups"]   = service_function_group_list
        
        sf_group_list =  ServiceFunctionGroup.objects.filter(service_function_chain=sfc_data.id)
        for sf_group in sf_group_list:
            temp_sf_group = {}
            temp_sf_group["id"]            = sf_group.id
            temp_sf_group["tenant_id"]     = sf_group.tenant_id
            temp_sf_group["name"]          = sf_group.name
            temp_sf_group["description"]   = sf_group.description
            service_function_list          = []
            temp_sf_group["service_functions"] = service_function_list
            service_function_group_list.append(temp_sf_group)
            
            sf_list = ServiceFunction.objects.filter(Service_function_groups=sf_group.id)
            for sf in sf_list:
                temp_sf = {}
                
                ingress_port = Port.objects.get(pk=sf.ingress)
                ingress_ovs_interface = OVSInterface.objects.filter(attached_mac=ingress_port.mac_address)
                egress_port = Port.objects.get(id=sf.egress)
                egress_ovs_interface = OVSInterface.objects.filter(attached_mac=egress_port.mac_address)
        
                temp_sf["id"] = sf.id
                temp_sf["tenant_id"] = sf.tenant_id
                temp_sf["name"] = sf.name
                temp_sf["description"] = sf.description
                temp_sf["ingress_port"] = ingress_port
                temp_sf["ingress_mac"] = ingress_port.mac_address
                temp_sf["ingress_of_port"] = ingress_ovs_interface[0].ofport
                
                temp_sf["egress_port"]  = egress_port
                temp_sf["egress_mac"]   = egress_port.mac_address
                temp_sf["egress_of_port"] = egress_ovs_interface[0].ofport
                temp_sf["service_function_parameters"] = sf.service_function_parameters
                service_function_list.append(temp_sf)
                
                
        flowclassifiers          = []
        params ["flowclassifiers"] = flowclassifiers
        
        flowclassifier_list = FlowClassifier.objects.filter(service_function_chain=sfc_data.id)
        print flowclassifier_list
        for flowclassifier in flowclassifier_list:
            temp_flowclassifier = {}
            logical_source_port = Port.objects.get(id=flowclassifier.logical_source_port)
            logical_source_ovs_interface = OVSInterface.objects.filter(attached_mac=logical_source_port.mac_address)
            
            temp_flowclassifier["id"] = flowclassifier.id 
            temp_flowclassifier["name"] = flowclassifier.name
            temp_flowclassifier["description"] = flowclassifier.description 
            temp_flowclassifier["ethertype"] = flowclassifier.ethertype 
            temp_flowclassifier["protocol"] = flowclassifier.protocol 
            temp_flowclassifier["source_port_range_min"] = flowclassifier.source_port_range_min 
            temp_flowclassifier["source_port_range_max"] = flowclassifier.source_port_range_max 
            temp_flowclassifier["destination_port_range_min"] = flowclassifier.destination_port_range_min 
            temp_flowclassifier["destination_port_range_max"] = flowclassifier.destination_port_range_max 
            temp_flowclassifier["source_ip_prefix"] = flowclassifier.source_ip_prefix
            temp_flowclassifier["destination_ip_prefix"] = flowclassifier.destination_ip_prefix
            temp_flowclassifier["logical_source_port"] = flowclassifier.logical_source_port
            temp_flowclassifier["logical_source_port_mac"] = logical_source_port.mac_address
            temp_flowclassifier["logical_source_port_of_port"] = logical_source_ovs_interface[0].ofport
            temp_flowclassifier["logical_destination_port"] = flowclassifier.logical_destination_port 
            temp_flowclassifier["l7_parameters"] = flowclassifier.l7_parameters
            flowclassifiers.append(temp_flowclassifier)
            
            
        ovs_bridges = []
        params ["ovs_bridges"] = ovs_bridges 
        
        br_ints = OVSBridge.objects.filter(name="br-int")
        for br_int in br_ints:
            temp_ovs_bridge = {}
            temp_ovs_bridge["dpid"] = br_int.datapath_id
            ovs_bridges.append(temp_ovs_bridge)
        
        return params
    
    def generate_sfc_rule (self,src_port, dest_port, flow_classifier,dpid):
        sfc_OF_entry_list = []
        
        ingress_OF_entry = {}
        ingress_OF_entry["switch"]      = dpid
        ingress_OF_entry["name"]        = "ingress"
        ingress_OF_entry["cookie"]      = 100
        ingress_OF_entry["priority"]    = 50
        ingress_OF_entry["eth_type"]    = "0x0800"
        ingress_OF_entry["active"]      = "true"
        ingress_OF_entry["in_port"]     = src_port["ofNum"]
        ingress_OF_entry["instruction_goto_table"] = "5"
        # we should implement flow classifier functon at this point
        
        sfc_OF_entry_list.append(ingress_OF_entry)
        
        modify_OF_entry = {}
        modify_OF_entry["switch"]       = dpid
        modify_OF_entry["name"]         = "table_5_mac_rewrite"
        modify_OF_entry["table"]        = 5
        modify_OF_entry["cookie"]       = 100
        modify_OF_entry["priority"]     = 50
        modify_OF_entry["active"]       = "true"
        modify_OF_entry["instruction_apply_actions"] = "set_field=eth_dst->"+dest_port["mac"]
        modify_OF_entry["instruction_goto_table"] = "10"
        sfc_OF_entry_list.append(modify_OF_entry)
        
        egress_OF_entry = {}
        egress_OF_entry["switch"]   = dpid
        egress_OF_entry["name"]     = "table_10_forwarding"
        egress_OF_entry["table"]    = "10"
        egress_OF_entry["cookie"]   = 100
        egress_OF_entry["priority"] = 50
        egress_OF_entry["eth_dst"]  = dest_port["mac"]
        egress_OF_entry["active"]   = "true"
        egress_OF_entry["instruction_apply_actions"] = "output="+dest_port["ofNum"]
        sfc_OF_entry_list.append(egress_OF_entry)
        return sfc_OF_entry_list
         
    def generate_sfc_rules(self,params):
        entire_sfc_rules = []
        for ovs_bridge in params["ovs_bridges"]:
            dpid =  ovs_bridge["dpid"][0:2]+":"+ovs_bridge["dpid"][2:4]+":"+ovs_bridge["dpid"][4:6]+":"+ovs_bridge["dpid"][6:8]+":"+ovs_bridge["dpid"][8:10]+":"+ovs_bridge["dpid"][10:12]+":"+ovs_bridge["dpid"][12:14]+":"+ovs_bridge["dpid"][14:16]
            
            src_port = {}
            src_port["mac"]     = params["flowclassifiers"][0]["logical_source_port_mac"]
            src_port["ofNum"]   = params["flowclassifiers"][0]["logical_source_port_of_port"]
            
            for service_function_group in params["service_function_groups"]: 
                for service_function in service_function_group["service_functions"]:
                    dest_port = {}
                    dest_port["mac"] = service_function["ingress_mac"]
                    dest_port["ofNum"] = service_function["ingress_of_port"]
                    sfc_rules = self.generate_sfc_rule (src_port,dest_port,params["flowclassifiers"][0],dpid)
                    entire_sfc_rules = entire_sfc_rules + sfc_rules
                    
                    src_port = {}
                    src_port["mac"]     = service_function["egress_mac"]
                    src_port["ofNum"]   = service_function["egress_of_port"]
        
        return entire_sfc_rules
        
    def active_sfc_rule(self,sfc_data):
        params = self.load_sfc_parameter(sfc_data)
        entire_sfc_rules = self.generate_sfc_rules (params)
        
        for sfc_rule in entire_sfc_rules:
            print "SFC Rule: %s" % sfc_rule
            r = requests.post('http://127.0.0.1:8080/wm/staticflowpusher/json', data = json.dumps(sfc_rule))
            print r.headers 
            print r.json()
        
        
    def create(self, request, *args, **kwargs):
        print "create"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
    
    def retrieve(self, request, pk=None):
        sfc_data = get_object_or_404(self.queryset, pk=pk)
        if sfc_data.active == "active":
            self.active_sfc_rule(sfc_data)
            
        elif sfc_data.active == "inactive":
            br_ints = OVSBridge.objects.filter(name="br-int")
            for br_int in br_ints:
                dpid =  br_int.datapath_id[0:2]+":"+br_int.datapath_id[2:4]+":"+br_int.datapath_id[4:6]+":"+br_int.datapath_id[6:8]+":"+br_int.datapath_id[8:10]+":"+br_int.datapath_id[10:12]+":"+br_int.datapath_id[12:14]+":"+br_int.datapath_id[14:16]
                r = requests.get('http://127.0.0.1:8080/wm/staticflowpusher/clear/'+dpid+'/json')
                print r.headers 
                print r.json()
            print "inactive"
        
        serializer = self.serializer_class(sfc_data)
        return Response(serializer.data)
    
    
    
    
class FlowClassifierViewSet(viewsets.ModelViewSet):
    queryset = FlowClassifier.objects.all()
    serializer_class = FlowClassifierSerializer
