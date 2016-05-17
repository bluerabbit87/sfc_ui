from django.core.exceptions import ObjectDoesNotExist
import json
import pprint
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
import socket
from time import sleep

from sdn_switch.models import OpenvSwitch, Host, OVSBridge, OVSPort, OVSInterface, \
    OVSBridge, OVSPort, OVSInterface
from sdn_switch.serializers import OpenvSwitchSerializer, HostSerializer, \
    OVSBridgeSerializer, OVSPortSerializer, OVSInterfaceSerializer


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

# Create your views here.

class HostViewSet(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    
    def check_status(self, host_info):
        try:
            self.ovsdbManager = OVSDBManager (host_info.mgmt_ip,host_info.mgmt_port)
            #results = ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Open_vSwitch","where":[]}])
        except socket.error as Detail:
            print type(Detail)
            host_info.status = type(Detail)
            host_info.save()
            return
        except Exception as Detail:
            print type(Detail)
            host_info.status = type(Detail)
            host_info.save()
            return
   
        host_info.status = "Good, Connected"
        host_info.save()  
    
    def UpdateOpenvSwitch(self, host_info):
        results = []
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Open_vSwitch","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return
         
        for result in results["result"]:
            for row in result["rows"]:
                try:
                    print "OVS Update"
                    new_ovs                 =  OpenvSwitch.objects.get(pk = row["_uuid"])
                    new_ovs.owner_Host      =  host_info
                    new_ovs._version        =  row["_version"]
                    new_ovs.bridges         =  row["bridges"]
                    new_ovs.cur_cfg         =  row["cur_cfg"]
                    new_ovs.db_version      =  row["db_version"]
                    new_ovs.external_ids    =  row["external_ids"]
                    new_ovs.manager_options =  row["manager_options"]
                    new_ovs.next_cfg        =  row["next_cfg"]
                    new_ovs.other_config    =  row["other_config"]
                    new_ovs.ovs_version     =  row["ovs_version"]
                    new_ovs.ssl             =  row["ssl"]
                    new_ovs.statistics      =  row["statistics"]
                    new_ovs.system_type     =  row["system_type"]
                    new_ovs.system_version  =  row["system_version"]
                    new_ovs.save()
                except ObjectDoesNotExist as detail:
                    print "OVS Add"
                    new_ovs = OpenvSwitch(
                                        _uuid           =  row["_uuid"],
                                        owner_Host      =  host_info,
                                        _version        =  row["_version"],
                                        bridges         =  row["bridges"],
                                        cur_cfg         =  row["cur_cfg"],
                                        db_version      =  row["db_version"],
                                        external_ids    =  row["external_ids"],
                                        manager_options =  row["manager_options"],
                                        next_cfg        =  row["next_cfg"],
                                        other_config    =  row["other_config"],
                                        ovs_version     =  row["ovs_version"],
                                        ssl             =  row["ssl"],
                                        statistics      =  row["statistics"],
                                        system_type     =  row["system_type"],
                                        system_version  =  row["system_version"],
                                          )
                    new_ovs.save()

    def UpdateOVSPort(self, host_info):
        results = []
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Port","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return
         
        for result in results["result"]:
            for row in result["rows"]:
                print row
                try:
                    print "Update OVS Port"
                    new_OVS_port = OVSPort.objects.get(pk = row["_uuid"])
                    new_OVS_port.bond_active_slave =  row["bond_active_slave"]
                    new_OVS_port.bond_downdelay = row["bond_downdelay"]
                    new_OVS_port.bond_fake_iface = row["bond_fake_iface"]
                    new_OVS_port.bond_mode = row["bond_mode"]
                    new_OVS_port.bond_updelay = row["bond_updelay"]
                    new_OVS_port.external_ids = row["external_ids"]
                    new_OVS_port.fake_bridge = row["fake_bridge"]
                    new_OVS_port.interfaces = row["interfaces"]
                    new_OVS_port.lacp = row["lacp"]
                    new_OVS_port.mac = row["mac"]
                    new_OVS_port.name = row["name"]
                    new_OVS_port.other_config = row["other_config"]
                    new_OVS_port.qos = row["qos"]
                    new_OVS_port.statistics = row["statistics"]
                    new_OVS_port.status = row["status"]
                    new_OVS_port.tag = row["tag"]
                    new_OVS_port.trunks = row["trunks"]
                    new_OVS_port.vlan_mode = row["vlan_mode"]
                    new_OVS_port.save()
                except ObjectDoesNotExist as Detail:
                    print "add OVS Port" 
                    new_OVS_port = OVSPort (_uuid = row["_uuid"], 
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
                    new_OVS_port.save()
            print "complete port update"
                                            
    def UpdateOVSInterface(self, host_info):
        results = []
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Interface","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return
         
        for result in results["result"]:
            for row in result["rows"]:
                print row
                try:
                    print "Update OVS Interface"
                    new_OVS_interface = OVSInterface.objects.get(pk = row["_uuid"])
                    new_OVS_interface.owner_host  = host_info
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
                    new_OVS_interface.save()
                    
                except ObjectDoesNotExist as Detail:
                    print "add OVS Interface" 
                    new_OVS_interface = OVSInterface (
                                                    _uuid = row["_uuid"],
                                                    owner_host  = host_info,
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
                                                    )
                    new_OVS_interface.save()                                         
    
    def UpdateOVSBridge(self, host_info):
        results = []
        try:
            results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Bridge","where":[]}])
        
        except Exception as Detail:
            print type(Detail)
            return
         
        for result in results["result"]:
            for row in result["rows"]:
                print row
                try:
                    print "Update OVS Bridge"
                    new_ovsbridge = OVSBridge.objects.get(pk = row["_uuid"])
                    new_ovsbridge.controller = row["controller"]
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
                                                controller = row["controller"],
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
    
    
    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
    

    def retrieve(self, request, pk=None):
        print "ovs retrieve"
        host_info = get_object_or_404(self.queryset, pk=pk)
        self.check_status(host_info)
        #self.UpdateOpenvSwitch(host_info)
        #self.UpdateOVSBridge(host_info)
        #self.UpdateOVSPort(host_info)
        self.UpdateOVSInterface(host_info)
        
        #self.update_ports(vim_environment)
        #self.update_hypervisors(vim_environment)
        #self.update_networks(vim_environment)
        #self.update_instances(vim_environment)
        serializer = self.serializer_class(host_info)
        return Response(serializer.data)    
    
class OpenvSwitchViewSet(viewsets.ModelViewSet):
    queryset = OpenvSwitch.objects.all()
    serializer_class = OpenvSwitchSerializer
    
class OVSPortViewSet(viewsets.ModelViewSet):
    queryset = OVSPort.objects.all()
    serializer_class = OVSPortSerializer    
    
class OVSBridgeViewSet(viewsets.ModelViewSet):
    queryset = OVSBridge.objects.all()
    serializer_class = OVSBridgeSerializer
    
class OVSInterfaceViewSet(viewsets.ModelViewSet):
    queryset = OVSInterface.objects.all()
    serializer_class = OVSInterfaceSerializer
