'''
Created on May 11, 2016

@author: root
'''
from rest_framework import serializers

from sdn_controllers.models import SDNController, OpenFlowSwitch,  \
    OpenFlowEntry, OpenFlowPort
from sdn_switch.models import OpenvSwitch, Host, OVSBridge, OVSPort, \
    OVSInterface
from sfc.models import service_function


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
                    "summary",
                    "host")
        
 
class OpenFlowSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenFlowSwitch
        fields = (      "dpid",                 
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
