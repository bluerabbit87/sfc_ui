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
    OpenFlowPort
from sdn_controllers.serializers import SDNControllerSerializer, \
    OpenFlowSwitchSerializer, OpenFlowEntrySerializer, OpenFlowPortSerializer


class OpenFlowHandler(object):
    ''' classdocs
    본 클래스는 Floodlgiht v1.1으로 부터 SDN 제어기의 상태, OpenFlow 스위치들의 상태를 
Floodlgiht에서 제공하는 아래의 RestAPI들을 호출하여 불러오는, 그리고 불러와서 Parsing
하는 역활을 합니다. 

Example: 

Request: http://127.0.0.1:8080/wm/core/switch/all/desc/json

Respond: 
 
{"00:00:00:00:00:00:00:03":{"desc":{"version":"OF_10","manufacturerDescription":
"Nicira Networks, Inc.","hardwareDescription":"Open vSwitch","softwareDescription":
"1.4.6","serialNumber":"None","datapathDescription":"None"}},"00:00:00:00:00:00:00:02
...
":"Nicira Networks, Inc.","hardwareDescription":"Open vSwitch","softwareDescription":"1.4.6",
"serialNumber":"None","datapathDescription":"None"}},"00:00:00:00:00:00:00:06":{"desc":{"}}}
    '''
    
    "Floodlight REST API URLs"
    url_switch_desc = '/wm/core/switch/all/desc/json'
    url_switch_port = '/wm/core/switch/all/port/json'
    url_switch_flow = '/wm/core/switch/all/flow/json'
    url_topology_link = '/wm/topology/links/json'
    url_device = '/wm/device'
    url_route = '/wm/topology/route'
    url_static_flow_pusher = '/wm/staticflowpusher/json'
    url_health = '/wm/core/health/json'

    def __init__(self, controller_ip, controller_port,logger = None): 
        '''
        Constructor
        A __init__ function receives connection information of SDN controller such as IP and Port addresses.
        FloodlightPlugin communicates with SND controller with above IP and Port addresses.
        '''
        
        self.__controller_ip = controller_ip;
        self.__controller_port = controller_port;
        
        if logger == None:
            self.logger = logging.getLogger('logger');
            fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
        
            streamHandler = logging.StreamHandler();
            streamHandler.setFormatter(fomatter);
            self.logger.addHandler(streamHandler);
                
                        # 로거 인스턴스의 로깅 레벨을 설정한다.
            fileHandler = logging.FileHandler("./OpenflowHendler.log");
            fileHandler.setFormatter(fomatter);
            self.logger.addHandler(fileHandler);
        
            self.logger.setLevel("DEBUG");
        else:
            self.logger = logger;
        # At this time, FloodlightPlugin communicates with Floodlight via a pycurl library
        
        
    def get_controller_ip(self):
        # Return the IP address of sdn controller  
        return self.__controller_ip
    
    def get_controller_port(self):
        # Return a Port address of this FloodlightPlugin  
        return self.__controller_port
    
    def get_route(self, src_switch_DPID, src_switch_port, dest_switch_DPID, dest_switch_port):
        url = self.url_route
        route_request_url = "%s/%s/%s/%s/%s/json" % (self.url_route, src_switch_DPID, src_switch_port, dest_switch_DPID, dest_switch_port)
        print route_request_url
        return self.__get(route_request_url)
    
    def static_flow_pusher_add(self, post_data):
        self.__post(self.url_static_flow_pusher, post_data)
    
    def static_flow_pusher_list(self, switch_dpid):
        return self.__get("/wm/staticflowpusher/list/%s/json" % (switch_dpid))
        
    def static_flow_pusher_clear(self, switch_dpid):
        return self.__get("/wm/staticflowpusher/clear/%s/json" % (switch_dpid))
    
    def __post(self, url, post_data):
        # by using pycurl, __get function returns the response of the requested url.   
        self.logger.info("by using pycurl, __get function returns the response of the requested url.");
        local_pycurl = pycurl.Curl()
        
        request_curl_url = "http://" + self.__controller_ip + ":" + self.__controller_port + url
        local_pycurl.setopt(local_pycurl.URL, request_curl_url)
        self.logger.debug("request_curl_url: " + request_curl_url);
                
        local_pycurl.setopt(pycurl.HTTPHEADER, ['X-Postmark-Server-Token: API_TOKEN_HERE', 'Accept: application/json'])
        local_pycurl.setopt(pycurl.POST, 1)
        
        data = json.dumps(post_data)
        local_pycurl.setopt(pycurl.POSTFIELDS, data)
        self.logger.debug("request_curl_post_data: " + data);
                
        
        buf = cStringIO.StringIO()
        local_pycurl.setopt(local_pycurl.WRITEFUNCTION, buf.write)
        
        try:
            local_pycurl.perform()
            local_pycurl.close()
        except pycurl.error:
            self.logger.critical("couldn't connect to host");
            return None
       
        raw_json_response = buf.getvalue()
        buf.close()
        
        # by using json library, it parses recieved raw json data to python data structure (e.g., list, dictionary)  
        json_response = json.loads(raw_json_response);
        self.logger.debug(json.dumps(json_response, sort_keys=True,
                         indent=4, separators=(',', ': ')));
        return json_response
       
    def __get(self, url):
        # by using pycurl, __get function returns the response of the requested url.   
        self.logger.info("by using pycurl, __get function returns the response of the requested url.");
        local_pycurl = pycurl.Curl()   
        buf = cStringIO.StringIO()
        request_curl_url = "http://" + self.__controller_ip + ":" + self.__controller_port + url
        self.logger.debug("request_curl_url: " + request_curl_url);
        local_pycurl.setopt(local_pycurl.URL, request_curl_url)
        local_pycurl.setopt(local_pycurl.WRITEFUNCTION, buf.write)
        try:
            local_pycurl.perform()
            local_pycurl.close()
        except pycurl.error:
            #self.logger.critical("couldn't connect to host");
            return None
            
        
        raw_json_response = buf.getvalue()
        buf.close()
        # by using json library, it parses recieved raw json data to python data structure (e.g., list, dictionary)  
        if raw_json_response != "":
            json_response = json.loads(raw_json_response);
            self.logger.debug(json.dumps(json_response, sort_keys=True,
                            indent=4, separators=(',', ': ')));
            return json_response
        
        else:
            self.logger.debug("There is no route for request info");
            return None
        
        
    def get_switch_desc(self):
        self.logger.info("get_switch_desc");
        return self.__get(self.url_switch_desc)
    
    def get_switch_port(self):
        self.logger.info("get_switch_port");
        return self.__get(self.url_switch_port)
    
    def get_switch_flow(self):
        self.logger.info("get_switch_flow");
        return self.__get(self.url_switch_flow)
        
    def get_topology_link(self):
        self.logger.info("get_topology_link");
        return self.__get(self.url_topology_link)
        
    def get_device(self):
        self.logger.info("get_device");
        return self.__get(self.url_device)

    def get_health(self):
        self.logger.info("get_health");
        return self.__get(self.url_health)

    def get_load_modules(self):
        self.logger.info("get_module");
        return self.__get("/wm/core/module/loaded/json")

    def get_memory(self):
        self.logger.info("get_memory");
        return self.__get("/wm/core/memory/json")
    
    def get_sys_uptime(self):
        self.logger.info("get_uptime");
        return self.__get("/wm/core/system/uptime/json")

    def get_tables(self):
        self.logger.info("get_tables");
        return self.__get("/wm/core/storage/tables/json")
 
    def get(self, url):
        return self.__get(url)
    
    def port(self, url, post_data):
        return self.__post(url, post_data)

# Create your views here.
class SDNControllerViewSet(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.CreateModelMixin,
               viewsets.GenericViewSet):
    queryset = SDNController.objects.all()
    serializer_class = SDNControllerSerializer
    
    url_switch_desc = '/wm/core/switch/all/desc/json'
    url_switch_port = '/wm/core/switch/all/port/json'
    url_switch_flow = '/wm/core/switch/all/flow/json'
    url_topology_link = '/wm/topology/links/json'
    url_device = '/wm/device'
    url_route = '/wm/topology/route'
    url_static_flow_pusher = '/wm/staticflowpusher/json'
    url_health = '/wm/core/health/json'
    
    def check_status(self, cont_info):
        connection_url = 'http://'+cont_info.mgmt_ip+":"+cont_info.mgmt_port
        
        health_response = requests.get(connection_url+self.url_health)
        if (health_response.status_code == 200):
            cont_info.health = health_response.json()
        else:
            cont_info.health = "unknown"
        
        memory_response = requests.get(connection_url+"/wm/core/memory/json")
        if (memory_response.status_code == 200):
            cont_info.memory = memory_response.json()
        else:
            cont_info.memory = "unknown"
        
        uptime_response = requests.get(connection_url+"/wm/core/system/uptime/json")
        if (uptime_response.status_code == 200):
            cont_info.uptime = uptime_response.json()
        else:
            cont_info.uptime = "unknown"
        
        tables_response = requests.get(connection_url+"/wm/core/storage/tables/json")
        if (tables_response.status_code == 200):
            cont_info.tables = tables_response.json()
        else:
            cont_info.tables = "unknown"
        
        role_response = requests.get(connection_url+"/wm/core/role/json")
        if (role_response.status_code == 200):
            cont_info.role = role_response.json()
        else:
            cont_info.role = "unknown"
        
        summary_response = requests.get(connection_url+"/wm/core/controller/summary/json")
        if (summary_response.status_code == 200):
            cont_info.summary = summary_response.json()
        else:
            cont_info.summary = "unknown"
        
        
        
        if ((health_response.status_code == 200) and
            (memory_response.status_code == 200) and
            (uptime_response.status_code == 200) and
            (tables_response.status_code == 200)):
            cont_info.status = "Good"
        else:
            cont_info.status = "unknown"    
        cont_info.save()
        
    def UpdateFloodlightSwitche(self, cont_info):
        url = 'http://'+cont_info.mgmt_ip+":"+cont_info.mgmt_port+"/wm/core/switch/all/desc/json"
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
                                                softwareDescription = value['desc']['softwareDescription'],
                                                datapathDescription = value['desc']['datapathDescription'],
                                                hardwareDescription = value['desc']['hardwareDescription'],
                                                manufacturerDescription = value['desc']['manufacturerDescription'],
                                                serialNumber = value['desc']['serialNumber'],
                                                version = value['desc']['version'])
                new_of_switch.save()

    def UpdateFloodlightPort(self, cont_info):
        url = 'http://'+cont_info.mgmt_ip+":"+cont_info.mgmt_port+"/wm/core/switch/all/port/json"
        print url
        response = requests.get(url)
        results = response.json()
        
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
                            #new_port.portNumber     = port["portNumber"]              
                            new_port.receiveBytes   = port["receiveBytes"]            
                            new_port.receiveCRCErrors = port["receiveCRCErrors"]        
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
    def UpdateFloodlightFlowEntry(self, cont_info):
        url = 'http://'+cont_info.mgmt_ip+":"+cont_info.mgmt_port+"/wm/core/switch/all/flow/json"
        print url
        response = requests.get(url)
        results = response.json()
        
        for (switch_dpid,values) in results.items():
            print (switch_dpid,values)
            for flow in values["flows"]:
                try:
                    if flow['version'] == u'OF_13':
                        new_flow = OpenFlowEntry.objects.get(owner_switch = switch_dpid, cookie = flow['cookie'],tableId = flow['tableId'], instructions = flow['instructions'])
                    else:
                        new_flow = OpenFlowEntry.objects.get(owner_switch = switch_dpid, cookie = flow['cookie'],tableId = flow['tableId'], instructions = flow['actions'])
                    
                    new_flow.priority           = flow['priority']
                    new_flow.durationNSeconds   = flow['durationNSeconds']
                    new_flow.idleTimeoutSec     = flow['idleTimeoutSec']
                    new_flow.durationSeconds    = flow['durationSeconds']
                    new_flow.version            = flow['version']
                    new_flow.byteCount          = flow['byteCount']
                    #new_flow.tableId            = flow['tableId']
                    new_flow.packetCount        = flow['packetCount']         
                    new_flow.hardTimeoutSec     = flow['hardTimeoutSec']
                    #new_flow.cookie             = flow['cookie']
                    #new_flow.match              = flow['match']
                    if flow['version'] == u'OF_13':
                        new_flow.flags          = flow['flags']
                    #    new_flow.instructions   = flow['instructions']
                    else:
                    #    new_flow.instructions        = flow['actions']
                        pass
                    new_flow.save()
                except ObjectDoesNotExist:
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


            #for value in values["flows"]:
            #    print 
            #    ports =  value["port"]
#                 for port in ports:
#                     print port
#                     try:
#                             new_port = OpenFlowPort.objects.get(owner_switch = switch_dpid, portNumber = port["portNumber"] )
#                             new_port.version        = value["version"]            
#                             new_port.collisions     = port["collisions"]              
#                             if (value["version"] == "OF_13"):
#                                 new_port.durationSec    = port["durationSec"]             
#                                 new_port.durationNsec   = port["durationNsec"]    
#                             #new_port.portNumber     = port["portNumber"]              
#                             new_port.receiveBytes   = port["receiveBytes"]            
#                             new_port.receiveCRCErrors = port["receiveCRCErrors"]        
#                             new_port.receiveDropped     = port["receiveDropped"]          
#                             new_port.receiveErrors      = port["receiveErrors"]           
#                             new_port.receiveFrameErrors = port["receiveFrameErrors"]      
#                             new_port.receiveOverrunErrors = port["receiveOverrunErrors"]    
#                             new_port.receivePackets     = port["receivePackets"]          
#                             new_port.transmitBytes      = port["transmitBytes"]           
#                             new_port.transmitDropped    = port["transmitDropped"]         
#                             new_port.transmitErrors     = port["transmitErrors"]          
#                             new_port.transmitPackets    = port["transmitPackets"]         
#                             new_port.save()
#                     except ObjectDoesNotExist:
#                         if (value["version"] == "OF_13"):
#                                 durationSec    = port["durationSec"]             
#                                 durationNsec   = port["durationNsec"]
#                         elif (value["version"] == "OF_10"):
#                                 durationSec    = "unknown"        
#                                 durationNsec   = "unknown"
#                             
#                         new_port        = OpenFlowPort (owner_switch = OpenFlowSwitch.objects.get(pk = switch_dpid),
#                                         portNumber      = port["portNumber"],
#                                         version        = value["version"],
#                                         collisions     = port["collisions"],              
#                                         durationNsec   = durationSec,            
#                                         durationSec    = durationNsec,                    
#                                         receiveBytes   = port["receiveBytes"],            
#                                         receiveCRCErrors = port["receiveCRCErrors"],        
#                                         receiveDropped     = port["receiveDropped"],         
#                                         receiveErrors      = port["receiveErrors"],           
#                                         receiveFrameErrors = port["receiveFrameErrors"],      
#                                         receiveOverrunErrors = port["receiveOverrunErrors"],    
#                                         receivePackets     = port["receivePackets"],          
#                                         transmitBytes      = port["transmitBytes"],           
#                                         transmitDropped    = port["transmitDropped"],         
#                                         transmitErrors     = port["transmitErrors"],          
#                                         transmitPackets    = port["transmitPackets"])
#                         new_port.save()            
            
    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
    

    def retrieve(self, request, pk=None):
        print "cont Controller retrieve"
        cont_info = get_object_or_404(self.queryset, pk=pk)
        #self.check_status(cont_info)
        #self.UpdateFloodlightSwitche(cont_info)
        #self.UpdateFloodlightPort(cont_info)
        self.UpdateFloodlightFlowEntry(cont_info)
        #self.update_instances(vim_environment)
        serializer = self.serializer_class(cont_info)
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