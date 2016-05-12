'''
Created on May 11, 2016

@author: root
'''
from rest_framework import serializers

from sdn_controllers.models import SDNController
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
                    "host")
    