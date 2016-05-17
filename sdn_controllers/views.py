# encoding: utf-8
import cStringIO
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
import json
import logging
import pprint
import pycurl
import requests
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from sdn_controllers.models import SDNController, OpenFlowSwitch, OpenFlowEntry, \
    OpenFlowPort, OpenFlowTopologyLink
from sdn_controllers.serializers import SDNControllerSerializer, \
    OpenFlowSwitchSerializer, OpenFlowEntrySerializer, OpenFlowPortSerializer,OpenFlowTopologyLinkSerializer
from optparse import Values


class SDNControllerViewSet(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    queryset = SDNController.objects.all()
    serializer_class = SDNControllerSerializer
    
    def __update_controller_status(self, controller_info):
        print "__update_controller_status is started"
        urls = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port
        
        try:
            health_response = requests.get(urls+'/wm/core/health/json')
            print health_response.json()
            controller_info.health = health_response.json()
            
            memory_response = requests.get(urls+"/wm/core/memory/json")
            print memory_response.json()
            controller_info.memory = memory_response.json()
        
            uptime_response = requests.get(urls+"/wm/core/system/uptime/json")
            print uptime_response.json()
            controller_info.uptime = uptime_response.json()
            
            tables_response = requests.get(urls+"/wm/core/storage/tables/json")
            print tables_response.json()
            controller_info.tables = tables_response.json()
    
            role_response = requests.get(urls+"/wm/core/role/json")
            print role_response.json()
            controller_info.role = role_response.json()
            
            summary_response = requests.get(urls+"/wm/core/controller/summary/json")
            print summary_response.json()
            controller_info.summary = summary_response.json()
    
            controller_info.status = "Good"
            controller_info.save()
            print "__update_controller_status is completed"
            return 0
        
        except Exception as detail:
            controller_info.status = detail.message
            controller_info.save()
            print "__update_controller_status is failure caused by %s" % detail.message
            return -1

    def __update_switches_status(self, controller_info):
        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/core/switch/all/desc/json"
        
        try:
            response = requests.get(url)
        except Exception as detail:
            controller_info.status = detail.message
            controller_info.save()
            print "__update_switches_status is failure caused by %s" % detail.message
            return -1
        result = response.json()
        print result
        for (dpid,value) in result.items():
            if value.has_key("desc"):
                try:
                    new_switch =  OpenFlowSwitch.objects.get(pk = dpid)
                    new_switch.softwareDescription = value['desc']['softwareDescription']
                    new_switch.datapathDescription = value['desc']['datapathDescription']
                    new_switch.hardwareDescription = value['desc']['hardwareDescription']
                    new_switch.manufacturerDescription = value['desc']['manufacturerDescription']
                    new_switch.serialNumber = value['desc']['serialNumber']
                    new_switch.version = value['desc']['version']
                    new_switch.save()
                    return 0
                except:
                    new_switch = OpenFlowSwitch(dpid = dpid,
                                                    owner_controller = controller_info,
                                                    softwareDescription = value['desc']['softwareDescription'],
                                                    datapathDescription = value['desc']['datapathDescription'],
                                                    hardwareDescription = value['desc']['hardwareDescription'],
                                                    manufacturerDescription = value['desc']['manufacturerDescription'],
                                                    serialNumber = value['desc']['serialNumber'],
                                                    version = value['desc']['version'])
                    new_switch.save()
                    return 0
            
        
    def __update_ports_status(self, controller_info):
        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/core/switch/all/port/json"
        try:
            response = requests.get(url)
        except Exception as detail:
            controller_info.status = detail.message
            controller_info.save()
            print "__update_ports_status is failure caused by %s" % detail.message
            return -1
        
        results = response.json()
        
        for (switch_dpid,values) in results.items():
            print values 
            if values.has_key("port_reply") == False:
                print "An error has occurred while proccesing your request"
            else:
                for value in values["port_reply"]:
                    for port in value["port"]:
                        if (value["version"] == "OF_13"):
                            durationSec    = port["durationSec"]             
                            durationNsec   = port["durationNsec"]
                        else:
                            durationSec    = "unknown"           
                            durationNsec   = "unknown"
                            
                        try:
                            new_port = OpenFlowPort.objects.get(owner_switch = switch_dpid, portNumber = port["portNumber"] )
                            new_port.version            = value["version"]            
                            new_port.collisions         = port["collisions"]              
                            new_port.durationSec        = durationSec             
                            new_port.durationNsec       = durationNsec   
                            new_port.receiveBytes       = port["receiveBytes"]            
                            new_port.receiveCRCErrors   = port["receiveCRCErrors"]        
                            new_port.receiveDropped     = port["receiveDropped"]          
                            new_port.receiveErrors      = port["receiveErrors"]           
                            new_port.receiveFrameErrors = port["receiveFrameErrors"]      
                            new_port.receiveOverrunErrors = port["receiveOverrunErrors"]    
                            new_port.receivePackets     = port["receivePackets"]          
                            new_port.transmitBytes      = port["transmitBytes"]           
                            new_port.transmitDropped    = port["transmitDropped"]         
                            new_port.transmitErrors     = port["transmitErrors"]          
                            new_port.transmitPackets    = port["transmitPackets"]         
                            new_port.save()
                            return 0
                        
                        except ObjectDoesNotExist:
                            new_port        = OpenFlowPort (owner_switch = OpenFlowSwitch.objects.get(pk = switch_dpid),
                                            portNumber      = port["portNumber"],
                                            version        = value["version"],
                                            collisions     = port["collisions"],              
                                            durationNsec   = durationSec,            
                                            durationSec    = durationNsec,                    
                                            receiveBytes   = port["receiveBytes"],            
                                            receiveCRCErrors = port["receiveCRCErrors"],        
                                            receiveDropped     = port["receiveDropped"],         
                                            receiveErrors      = port["receiveErrors"],           
                                            receiveFrameErrors = port["receiveFrameErrors"],      
                                            receiveOverrunErrors = port["receiveOverrunErrors"],    
                                            receivePackets     = port["receivePackets"],          
                                            transmitBytes      = port["transmitBytes"],           
                                            transmitDropped    = port["transmitDropped"],         
                                            transmitErrors     = port["transmitErrors"],          
                                            transmitPackets    = port["transmitPackets"])
                            new_port.save()
                            return 0

    def __update_topology_link_status (self, controller_info):
        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/topology/links/json"
        try:
            response = requests.get(url)
        except Exception as detail:
            controller_info.status = detail.message
            controller_info.save()
            print "__update_topology_link_status is failure"
            return -1
            
        results = response.json()
        OpenFlowTopologyLink.objects.filter(owner_controller=controller_info).delete()
        
        for value in results:
            if value.has_key("src-port") == True:
                new_link =  OpenFlowTopologyLink(owner_controller=controller_info,
                                                        direction = value['direction'],
                                                        src_port = value['src-port'],
                                                        src_switch = value['src-switch'],
                                                        dst_port= value['dst-port'],
                                                        dst_switch = value['dst-switch'],
                                                        type = value['type'])
                new_link.save()
                                                  
    def __update_flow_entry(self, controller_info):
        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/core/switch/all/flow/json"
        try:
            response = requests.get(url)
        except Exception as detail:
            controller_info.status = detail.message
            controller_info.save()
            print "__update_flow_entry is failure"
            return -1
        
        results = response.json()
        
        for (switch_dpid,values) in results.items():
            OpenFlowEntry.objects.filter(owner_switch = switch_dpid).delete()
            if values.has_key("flows") == False:
                print Values
                pass
            else:
                for flow in values["flows"]:
                    if flow['version'] == u'OF_13':
                        flags          = flow['flags']
                        instructions   = flow['instructions']
                    else:
                        flags           = "known"
                        instructions    = flow['actions']
                    new_flow = OpenFlowEntry(owner_switch = OpenFlowSwitch.objects.get(pk=switch_dpid),
                                            priority           = flow['priority'],
                                            durationNSeconds   = flow['durationNSeconds'],
                                            idleTimeoutSec     = flow['idleTimeoutSec'],
                                            durationSeconds    = flow['durationSeconds'],
                                            byteCount          = flow['byteCount'],
                                            tableId            = flow['tableId'],
                                            version            = flow['version'],
                                            packetCount        = flow['packetCount'],   
                                            hardTimeoutSec     = flow['hardTimeoutSec'],
                                            cookie             = flow['cookie'],
                                            match              = flow['match'],
                                            flags              = flags,
                                            instructions       = instructions)
                    new_flow.save()
            
 
    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
    

    def retrieve(self, request, pk=None):
        controller_info = get_object_or_404(self.queryset, pk=pk)
        
        result = self.__update_controller_status(controller_info)
        if result == -1:
            print "__update_controller_status is failure"
            serializer = self.serializer_class(controller_info)
            return Response(serializer.data)
         
        result = self.__update_ports_status(controller_info)
        if result == -1:
            print "__update_ports_status is failure"
            serializer = self.serializer_class(controller_info)
            return Response(serializer.data)
         
        result = self.__update_switches_status(controller_info)
        if result == -1:
            print "__update_switches_status is failure"
            serializer = self.serializer_class(controller_info)
            return Response(serializer.data)
        
        result = self.__update_topology_link_status(controller_info)
        if result == -1:
            print "__update_topology_link_status is failure"
            serializer = self.serializer_class(controller_info)
            return Response(serializer.data)
   
        result = self.__update_flow_entry(controller_info)
        if result == -1:
            print "__update_flow_entry is failure"
            serializer = self.serializer_class(controller_info)
            return Response(serializer.data)

        serializer = self.serializer_class(controller_info)
        return Response(serializer.data)
    

class OpenFlowSwitchViewSet(viewsets.ModelViewSet):
    queryset = OpenFlowSwitch.objects.all()
    serializer_class = OpenFlowSwitchSerializer

class OpenFlowEntryViewSet(viewsets.ModelViewSet):
    queryset = OpenFlowEntry.objects.all()
    serializer_class = OpenFlowEntrySerializer
    
class OpenFlowPortViewSet(viewsets.ModelViewSet):
    queryset = OpenFlowPort.objects.all()
    serializer_class = OpenFlowPortSerializer

class OpenFlowTopologyLinkViewSet(viewsets.ModelViewSet):
    queryset = OpenFlowTopologyLink.objects.all()
    serializer_class = OpenFlowTopologyLinkSerializer