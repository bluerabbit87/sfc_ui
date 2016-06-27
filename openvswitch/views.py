from django.core.exceptions import ObjectDoesNotExist
import json
import pprint
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
import socket
from time import sleep

from openvswitch.models import OpenvSwitch, OVSBridge, OVSPort, OVSInterface, \
    OVSBridge, OVSPort, OVSInterface, OVSController
from openvswitch.serializers import OpenvSwitchSerializer, \
    OVSBridgeSerializer, OVSPortSerializer, OVSInterfaceSerializer, \
    OVSControllerSerializer
from floodlight.models import SDNController


class OVSDBManager(object):
    '''
    classdocs
    '''
    def __init__(self, ip_, port_):
        '''
        Constructor
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip_, int(port_)))
         
    def query(self, json_data):
        self.s.send(json.dumps(json_data))
        result = ""
        while (True):
            response = self.s.recv(4096)
            result = result + response
            try:
                json_result = json.loads(result)
                return json_result
            except:
                print ""
             
    def listDB(self):
        listDB = {"method":"list_dbs", "params":[], "id": 0}
        return self.query(listDB)
     
    def getSchema(self):
        Get_Schema = {"method":"get_schema", "params":["Open_vSwitch"], "id": 0}
        return self.query(Get_Schema)
     
    def transact(self,params):
        Transact            =   {"method":"transact", "params":[], "id": 0}
        Transact["params"]  =   params
        return self.query(Transact)
     
    def monitor(self,params):
        Monitor             = {'id': 100, 'method': 'monitor', 'params': ""}
        Monitor["params"] = params
         
        return self.query(Monitor)
     
    def run(self):
        i=0
        while(True):
            sleep(1)
            result = ""
            while (True):
                response = self.s.recv(4096)
                result = result + response
                try:
                    json_result = json.loads(result)
                    print json_result
                    break
                except:
                    print ""
            print result

class OpenvSwitchViewSet(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    queryset = OpenvSwitch.objects.all()
    serializer_class = OpenvSwitchSerializer
    
    def check_status(self, ovs_info):
        try:
            self.ovsdbManager = OVSDBManager (ovs_info.mgmt_ip,ovs_info.mgmt_port)
        except socket.error as Detail:
            print type(Detail)
            ovs_info.status = type(Detail)
            ovs_info.save()
            return
        except Exception as Detail:
            print type(Detail)
            ovs_info.status = type(Detail)
            ovs_info.save()
            return
   
        ovs_info.status = "Good, Connected"
        ovs_info.save()  
    
    def UpdateOpenvSwitch(self, ovs_info):
        
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Open_vSwitch","where":[]}])
        except Exception as Detail:
            print type(Detail)
            return -1
        
        for result in results["result"]:
            for row in result["rows"]:
                ovs_info._uuid           =  row["_uuid"]
                ovs_info._version        =  row["_version"]
                ovs_info.bridges         =  row["bridges"]
                ovs_info.cur_cfg         =  row["cur_cfg"]
                ovs_info.db_version      =  row["db_version"]
                ovs_info.external_ids    =  row["external_ids"]
                ovs_info.manager_options =  row["manager_options"]
                ovs_info.next_cfg        =  row["next_cfg"]
                ovs_info.other_config    =  row["other_config"]
                ovs_info.ovs_version     =  row["ovs_version"]
                ovs_info.ssl             =  row["ssl"]
                ovs_info.statistics      =  row["statistics"]
                ovs_info.system_type     =  row["system_type"]
                ovs_info.system_version  =  row["system_version"]
                ovs_info.save()
        
        return 0

    def UpdateOVSPort(self, ovs_info):
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Port","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return -1
         
        for result in results["result"]:
            for row in result["rows"]:
                print row
                try:
                    new_ovs_port = OVSPort.objects.get(pk = row["_uuid"])
                    new_ovs_port.owner_ovs = ovs_info
                    new_ovs_port.bond_active_slave =  row["bond_active_slave"]
                    new_ovs_port.bond_downdelay = row["bond_downdelay"]
                    new_ovs_port.bond_fake_iface = row["bond_fake_iface"]
                    new_ovs_port.bond_mode = row["bond_mode"]
                    new_ovs_port.bond_updelay = row["bond_updelay"]
                    new_ovs_port.external_ids = row["external_ids"]
                    new_ovs_port.fake_bridge = row["fake_bridge"]
                    new_ovs_port.interfaces = row["interfaces"]
                    new_ovs_port.lacp = row["lacp"]
                    new_ovs_port.mac = row["mac"]
                    new_ovs_port.name = row["name"]
                    new_ovs_port.other_config = row["other_config"]
                    new_ovs_port.qos = row["qos"]
                    new_ovs_port.statistics = row["statistics"]
                    new_ovs_port.status = row["status"]
                    new_ovs_port.tag = row["tag"]
                    new_ovs_port.trunks = row["trunks"]
                    new_ovs_port.vlan_mode = row["vlan_mode"]
                    new_ovs_port.save()
                except ObjectDoesNotExist as Detail:
                    new_ovs_port = OVSPort (_uuid = row["_uuid"], 
                                            owner_ovs = ovs_info,
                                            bond_active_slave =  row["bond_active_slave"],
                                            bond_downdelay = row["bond_downdelay"],
                                            bond_fake_iface = row["bond_fake_iface"],
                                            bond_mode = row["bond_mode"],
                                            bond_updelay = row["bond_updelay"],
                                            external_ids = row["external_ids"],
                                            fake_bridge = row["fake_bridge"],
                                            interfaces = row["interfaces"],
                                            lacp = row["lacp"],
                                            mac = row["mac"],
                                            name = row["name"],
                                            other_config = row["other_config"],
                                            qos = row["qos"],
                                            statistics = row["statistics"],
                                            status = row["status"],
                                            tag = row["tag"],
                                            trunks = row["trunks"],
                                            vlan_mode = row["vlan_mode"])
                    new_ovs_port.save()
            return 0
                                            
    def UpdateOVSInterface(self, ovs_info):
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Interface","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return -1
         
        for result in results["result"]:
            for row in result["rows"]:
                self.attached_mac = ""
                self.iface_id     = ""
                self.iface_status = ""
                self.vm_uuid      = ""
                for entry in row["external_ids"]:
                    print entry
                    if entry != "map":
                        for entry_attribute in entry:
                            value = entry_attribute.pop()
                            key = entry_attribute.pop()
                            if key == 'attached-mac' :
                                self.attached_mac = value
                            elif key == 'iface-id' :
                                self.iface_id = value
                            elif key == 'iface-status' :
                                self.iface_status = value
                            elif key == 'vm-uuid' :
                                self.vm_uuid = value
                            print "key: %s, value: %s" % (key, value)
                
                try:
                    print "Update OVS Interface"
                    new_OVS_interface = OVSInterface.objects.get(pk = row["_uuid"])
                    new_OVS_interface.owner_ovs  = ovs_info
                    new_OVS_interface.admin_state = row["admin_state"]
                    new_OVS_interface.bfd =row["bfd"]
                    new_OVS_interface.bfd_status =row["bfd_status"]
                    new_OVS_interface.cfm_fault =row["cfm_fault"]
                    new_OVS_interface.cfm_fault_status =row["cfm_fault_status"]
                    new_OVS_interface.cfm_flap_count =row["cfm_flap_count"]
                    new_OVS_interface.cfm_health =row["cfm_health"]
                    new_OVS_interface.cfm_mpid =row["cfm_mpid"]
                    new_OVS_interface.cfm_remote_mpids =row["cfm_remote_mpids"]
                    new_OVS_interface.cfm_remote_opstate =row["cfm_remote_opstate"]
                    new_OVS_interface.duplex =row["duplex"]
                    new_OVS_interface.external_ids =row["external_ids"]
                    new_OVS_interface.link_speed =row["link_speed"]
                    new_OVS_interface.link_state =row["link_state"]
                    new_OVS_interface.mac =row["mac"]
                    new_OVS_interface.mac_in_use =row["mac_in_use"]
                    new_OVS_interface.mtu =row["mtu"]
                    new_OVS_interface.name =row["name"]
                    new_OVS_interface.ofport =row["ofport"]
                    new_OVS_interface.ofport_request =row["ofport_request"]
                    new_OVS_interface.options =row["options"]
                    new_OVS_interface.other_config =row["other_config"]
                    new_OVS_interface.statistics =row["statistics"]
                    new_OVS_interface.attached_mac = self.attached_mac
                    new_OVS_interface.iface_id     = self.iface_id
                    new_OVS_interface.iface_status = self.iface_status
                    new_OVS_interface.vm_uuid      = self.vm_uuid
                    
                    new_OVS_interface.save()
                    
                except ObjectDoesNotExist as Detail:
                    new_OVS_interface = OVSInterface (
                                                    _uuid = row["_uuid"],
                                                    owner_ovs  = ovs_info,
                                                    admin_state = row["admin_state"],
                                                    bfd =row["bfd"],
                                                    bfd_status =row["bfd_status"],
                                                    cfm_fault =row["cfm_fault"],
                                                    cfm_fault_status =row["cfm_fault_status"],
                                                    cfm_flap_count =row["cfm_flap_count"],
                                                    cfm_health =row["cfm_health"],
                                                    cfm_mpid =row["cfm_mpid"],
                                                    cfm_remote_mpids =row["cfm_remote_mpids"],
                                                    cfm_remote_opstate =row["cfm_remote_opstate"],
                                                    duplex =row["duplex"],
                                                    external_ids =row["external_ids"],
                                                    link_speed =row["link_speed"],
                                                    link_state =row["link_state"],
                                                    mac =row["mac"],
                                                    mac_in_use =row["mac_in_use"],
                                                    mtu =row["mtu"],
                                                    name =row["name"],
                                                    ofport =row["ofport"],
                                                    ofport_request =row["ofport_request"],
                                                    options =row["options"],
                                                    other_config =row["other_config"],
                                                    statistics =row["statistics"],
                                                    attached_mac = self.attached_mac,
                                                    iface_id     = self.iface_id,
                                                    iface_status = self.iface_status,
                                                    vm_uuid      = self.vm_uuid
                                                    )
                    new_OVS_interface.save()
        return 0                                    
    
    def UpdateOVSBridge(self, ovs_info):
        print type(ovs_info)
        results = []
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Bridge","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return -1
         
        for result in results["result"]:
            for row in result["rows"]:
                print row
                try:
                    try :
                        controller = OVSController.objects.get(pk = row["controller"])
                    except ObjectDoesNotExist:
                        controller = None
                        
                    print "Update OVS Bridge"
                    new_ovsbridge = OVSBridge.objects.get(pk = row["_uuid"])
                    new_ovsbridge.owner_ovs     = ovs_info
                    new_ovsbridge.controller    = controller
                    new_ovsbridge.datapath_id = row["datapath_id"]
                    new_ovsbridge.datapath_type = row["datapath_type"]
                    new_ovsbridge.external_ids = row["external_ids"]
                    new_ovsbridge.fail_mode = row["fail_mode"]
                    new_ovsbridge.flood_vlans = row["flood_vlans"]
                    new_ovsbridge.flow_tables = row["flow_tables"]
                    new_ovsbridge.ipfix = row["ipfix"]
                    new_ovsbridge.mirrors = row["mirrors"]
                    new_ovsbridge.name = row["name"]
                    new_ovsbridge.netflow = row["netflow"]
                    new_ovsbridge.other_config = row["other_config"]
                    new_ovsbridge.ports = row["ports"]
                    new_ovsbridge.protocols = row["protocols"]
                    new_ovsbridge.sflow = row["sflow"]
                    new_ovsbridge.status = row["status"]
                    new_ovsbridge.stp_enable = row["stp_enable"]
                    new_ovsbridge.save()
                except ObjectDoesNotExist as Detail:
                    print "add OVS Bridge" 
                    new_ovsbridge = OVSBridge(
                                                _uuid = row["_uuid"],
                                                controller = controller,
                                                owner_ovs = ovs_info,
                                                datapath_id = row["datapath_id"],
                                                datapath_type = row["datapath_type"],
                                                external_ids = row["external_ids"],
                                                fail_mode = row["fail_mode"],
                                                flood_vlans = row["flood_vlans"],
                                                flow_tables = row["flow_tables"],
                                                ipfix = row["ipfix"],
                                                mirrors = row["mirrors"],
                                                name = row["name"],
                                                netflow = row["netflow"],
                                                other_config = row["other_config"],
                                                ports = row["ports"],
                                                protocols = row["protocols"],
                                                sflow = row["sflow"],
                                                status = row["status"],
                                                stp_enable = row["stp_enable"],
                                              )
                    new_ovsbridge.save()
        return 0

    def UpdateOVSController(self, ovs_info):
        results = []
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Controller","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return -1
        
        pprint.pprint(results)
        
        for result in results["result"]:
            for values in result["rows"]:
                try:
                    new_controller = OVSController.objects.get(pk = values['_uuid'])
                    new_controller._version                 = values[u'_version']
                    new_controller.owner_ovs                = ovs_info
                    new_controller.connection_mode          = values[u'connection_mode']
                    new_controller.controller_burst_limit   = values[u'controller_burst_limit']
                    new_controller.controller_rate_limit    = values[u'controller_rate_limit']
                    new_controller.enable_async_messages    = values[u'enable_async_messages']
                    new_controller.external_ids             = values[u'external_ids']
                    new_controller.inactivity_probe         = values[u'inactivity_probe']
                    new_controller.is_connected             = values[u'is_connected']
                    new_controller.local_gateway            = values[u'local_gateway']
                    new_controller.local_ip                 = values[u'local_ip']
                    new_controller.local_netmask            = values[u'local_netmask']
                    new_controller.max_backoff              = values[u'max_backoff']
                    new_controller.other_config             = values[u'other_config']
                    new_controller.role                     = values[u'role']
                    new_controller.status                   = values[u'status']
                    new_controller.target                   = values[u'target']
                    new_controller.save()
                except ObjectDoesNotExist:
                    new_controller = OVSController(_uuid = values['_uuid'],
                                _version                 = values[u'_version'],
                                owner_ovs                = ovs_info,
                                connection_mode          = values[u'connection_mode'],
                                controller_burst_limit   = values[u'controller_burst_limit'],
                                controller_rate_limit    = values[u'controller_rate_limit'],
                                enable_async_messages    = values[u'enable_async_messages'],
                                external_ids             = values[u'external_ids'],
                                inactivity_probe         = values[u'inactivity_probe'],
                                is_connected             = values[u'is_connected'],
                                local_gateway            = values[u'local_gateway'],
                                local_ip                 = values[u'local_ip'],
                                local_netmask            = values[u'local_netmask'],
                                max_backoff              = values[u'max_backoff'],
                                other_config             = values[u'other_config'],
                                role                     = values[u'role'],
                                status                   = values[u'status'],
                                target                   = values[u'target'])
                    new_controller.save()    
        return 0
    
    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
    

    def retrieve(self, request, pk=None):
        print "ovs retrieve"
        ovs_info = get_object_or_404(self.queryset, pk=pk)
        self.check_status(ovs_info)
        self.UpdateOpenvSwitch(ovs_info)
        self.UpdateOVSBridge(ovs_info)
        self.UpdateOVSPort(ovs_info)
        self.UpdateOVSInterface(ovs_info)
        self.UpdateOVSController(ovs_info)
        serializer = self.serializer_class(ovs_info)
        return Response(serializer.data)    
    

    
class OVSPortViewSet(viewsets.ModelViewSet):
    queryset = OVSPort.objects.all()
    serializer_class = OVSPortSerializer    
    
class OVSBridgeViewSet(viewsets.ModelViewSet):
    queryset = OVSBridge.objects.all()
    serializer_class = OVSBridgeSerializer
    
class OVSInterfaceViewSet(viewsets.ModelViewSet):
    queryset = OVSInterface.objects.all()
    serializer_class = OVSInterfaceSerializer
    
class OVSControllerViewSet(viewsets.ModelViewSet):
    queryset = OVSController.objects.all()
    serializer_class = OVSControllerSerializer
