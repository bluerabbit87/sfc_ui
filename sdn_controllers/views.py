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
        
    def __update_ports_status(self, controller_info):

        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/core/switch/all/port/json"
        try:
            response = requests.get(url)
            results = response.json()
        except Exception as detail:
            controller_info.status = detail.message
            controller_info.save()
            print "__update_ports_status is failure caused by %s" % detail.message
            return -1
        
        for (switch_dpid,values) in results.items():
            print switch_dpid
            for value in values["port_reply"]:
                ports =  value["port"]
                for port in ports:
                    print port
                    try:
                            new_port = OpenFlowPort.objects.get(owner_switch = switch_dpid, portNumber = port["portNumber"] )
                            new_port.version        = value["version"]            
                            new_port.collisions     = port["collisions"]              
                            if (value["version"] == "OF_13"):
                                new_port.durationSec    = port["durationSec"]             
                                new_port.durationNsec   = port["durationNsec"]    
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

                    except ObjectDoesNotExist:
                        if (value["version"] == "OF_13"):
                                durationSec    = port["durationSec"]             
                                durationNsec   = port["durationNsec"]
                        elif (value["version"] == "OF_10"):
                                durationSec    = "unknown"        
                                durationNsec   = "unknown"
                            
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

    def UpdateFloodlightTopologyLink(self, controller_info):
        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/topology/links/json"
        try:
            response = requests.get(url)
            results = response.json()
        except Exception as detail:
            controller_info.status = detail.message
            controller_info.save()
        
        OpenFlowTopologyLink.objects.filter(owner_controller=controller_info).delete()
        for value in results:
            newTopologyLink =  OpenFlowTopologyLink(owner_controller=controller_info,
                                                    direction = value['direction'],
                                                    src_port = value['src_port'],
                                                    src_switch = value['src_switch'],
                                                    dst_port= value['dst_port'],
                                                    dst_switch = value['dst_switch'],
                                                    type = value['type'])
            newTopologyLink.save()
         
    def UpdateFloodlightSwitche(self, controller_info):
        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/core/switch/all/desc/json"
        response = requests.get(url)
        result = response.json()
        
        for (key,value) in result.items():
            try:
                print key
                new_of_switch =  OpenFlowSwitch.objects.get(pk = key)
                
                new_of_switch.softwareDescription = value['desc']['softwareDescription']
                new_of_switch.datapathDescription = value['desc']['datapathDescription']
                new_of_switch.hardwareDescription = value['desc']['hardwareDescription']
                new_of_switch.manufacturerDescription = value['desc']['manufacturerDescription']
                new_of_switch.serialNumber = value['desc']['serialNumber']
                new_of_switch.version = value['desc']['version']
                new_of_switch.save()
                
            except:
                new_of_switch = OpenFlowSwitch(dpid = key,
                                                owner_controller = controller_info,
                                                softwareDescription = value['desc']['softwareDescription'],
                                                datapathDescription = value['desc']['datapathDescription'],
                                                hardwareDescription = value['desc']['hardwareDescription'],
                                                manufacturerDescription = value['desc']['manufacturerDescription'],
                                                serialNumber = value['desc']['serialNumber'],
                                                version = value['desc']['version'])
                new_of_switch.save()

    
                                                
    def UpdateFloodlightFlowEntry(self, controller_info):
        url = 'http://'+controller_info.mgmt_ip+":"+controller_info.mgmt_port+"/wm/core/switch/all/flow/json"
        print url
        response = requests.get(url)
        results = response.json()
        print results
        for (switch_dpid,values) in results.items():
            print (switch_dpid,values)
            print "Delete OpenFlow Entris"
            OpenFlowEntry.objects.filter(owner_switch = switch_dpid).delete()
            
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
        
        
        #self.UpdateFloodlightSwitche(controller_info)
        #self.UpdateFloodlightFlowEntry(controller_info)
        #self.UpdateFloodlightTopologyLink(controller_info)
        #self.update_instances(vim_environment)
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