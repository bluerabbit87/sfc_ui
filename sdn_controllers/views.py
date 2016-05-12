# encoding: utf-8
import cStringIO
from django.shortcuts import render
import json
import logging
import pprint
import pycurl
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings

from sdn_controllers.models import SDNController
from sdn_controllers.serializers import SDNControllerSerializer


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
    
    def check_status(self, host_info):
        try:
            openflow = OpenFlowHandler(host_info.mgmt_ip,host_info.mgmt_port)
            host_info.health = openflow.get_health()
            host_info.memory = openflow.get_memory()
            host_info.uptime = openflow.get_sys_uptime()
            host_info.tables = openflow.get_tables()
            host_info.status = "Good"
            host_info.save()
        except Exception:
            host_info.status = "Not, Good"
            host_info.save()
    
    
    def UpdateFloodlightSwitche(self, host_info):
        openflow = OpenFlowHandler(host_info.mgmt_ip,host_info.mgmt_port)
#         result = openflow.get_switch_desc()
#         print result
#         result = openflow.get_switch_flow()
#         print result
        result = openflow.get_switch_port()
        print result

        #pprint.pprint (result)
        
#         
#          
#                                                 _uuid = row["_uuid"],
#                                                 controller = row["controller"],
#                                                 datapath_id = row["datapath_id"],
#                                                 datapath_type = row["datapath_type"],
#                                                 external_ids = row["external_ids"],
#                                                 fail_mode = row["fail_mode"],
#                                                 flood_vlans = row["flood_vlans"],
#                                                 flow_tables = row["flow_tables"],
#                                                 ipfix = row["ipfix"],
#                                                 mirrors = row["mirrors"],
#                                                 name = row["name"],
#                                                 netflow = row["netflow"],
#                                                 other_config = row["other_config"],
#                                                 ports = row["ports"],
#                                                 protocols = row["protocols"],
#                                                 sflow = row["sflow"],
#                                                 status = row["status"],
#                                                 stp_enable = row["stp_enable"],
#                                               )
#                     new_ovsbridge = OVSBridge(
#                     new_ovsbridge = OVSBridge.objects.get(pk = row["_uuid"])
#                     new_ovsbridge.controller = row["controller"]
#                     new_ovsbridge.datapath_id = row["datapath_id"]
#                     new_ovsbridge.datapath_type = row["datapath_type"]
#                     new_ovsbridge.external_ids = row["external_ids"]
#                     new_ovsbridge.fail_mode = row["fail_mode"]
#                     new_ovsbridge.flood_vlans = row["flood_vlans"]
#                     new_ovsbridge.flow_tables = row["flow_tables"]
#                     new_ovsbridge.ipfix = row["ipfix"]
#                     new_ovsbridge.mirrors = row["mirrors"]
#                     new_ovsbridge.name = row["name"]
#                     new_ovsbridge.netflow = row["netflow"]
#                     new_ovsbridge.other_config = row["other_config"]
#                     new_ovsbridge.ports = row["ports"]
#                     new_ovsbridge.protocols = row["protocols"]
#                     new_ovsbridge.save()
#                     new_ovsbridge.save()
#                     new_ovsbridge.sflow = row["sflow"]
#                     new_ovsbridge.status = row["status"]
#                     new_ovsbridge.stp_enable = row["stp_enable"]
#                     print "Update OVS Bridge"
#                     print "add OVS Bridge" 
#                 except ObjectDoesNotExist as Detail:
#                 print row
#                 try:
#             for row in result["rows"]:
#             print type(Detail)
#             results = self.ovsdbManager.transact(["Open_vSwitch",{"op":"select","table":"Bridge","where":[]}])
#             return
#         except Exception as Detail:
#         for result in results["result"]:
#         results = []
#         try:
#     def UpdateOVSBridge(self, host_info):
    
    
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
        self.check_status(cont_info)
        self.UpdateFloodlightSwitche(cont_info)
        #self.update_instances(vim_environment)
        serializer = self.serializer_class(cont_info)
        return Response(serializer.data)    