'''
Created on May 11, 2016

@author: root
'''
from rest_framework import serializers

from sdn_controllers.models import SDNController, OpenFlowSwitch, \
    OpenFlowEntry, OpenFlowPort, OpenFlowTopologyLink

class SDNControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDNController
        fields = (  "id",
                    "mgmt_ip",
                    "mgmt_port",
                    "status",
                    "health",
                    "memory",
                    "uptime",
                    "tables",
                    "role",
                    "summary")
        
 
class OpenFlowSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenFlowSwitch
        fields = (      "owner_controller",      
                        "dpid",                 
                        "datapathDescription",     
                        "hardwareDescription",     
                        "manufacturerDescription", 
                        "serialNumber",            
                        "softwareDescription",     
                        "version")
    
class OpenFlowEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenFlowEntry
        fields = (
                    "owner_switch",
                    "byteCount",           
                    "cookie",                  
                    "durationNSeconds",        
                    "durationSeconds",         
                    "flags",                   
                    "hardTimeoutSec",          
                    "idleTimeoutSec",          
                    "instructions",            
                    "match",                   
                    "packetCount",             
                    "priority",                
                    "tableId",                
                    "version")

class OpenFlowPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenFlowPort
        fields = (
                    "owner_switch",
                    "version",  
                    "collisions",              
                    "durationNsec",            
                    "durationSec",             
                    "portNumber",              
                    "receiveBytes",            
                    "receiveCRCErrors",        
                    "receiveDropped",          
                    "receiveErrors",           
                    "receiveFrameErrors",      
                    "receiveOverrunErrors",    
                    "receivePackets",          
                    "transmitBytes",           
                    "transmitDropped",         
                    "transmitErrors",          
                    "transmitPackets"         
                  )
        
class OpenFlowTopologyLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenFlowTopologyLink
        fields = (
                "owner_controller",
                "direction",               
                "src_port",                
                "src_switch",              
                "dst_port",                
                "dst_switch",              
                "type")                    