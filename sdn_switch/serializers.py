'''
Created on May 11, 2016

@author: root
'''
from rest_framework import serializers

from sdn_switch.models import OpenvSwitch, Host, OVSBridge, OVSPort, \
    OVSInterface
from sfc.models import service_function


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = (  "id",
                    "mgmt_ip",
                    "mgmt_port",
                    "mgmt_id",
                    "mgmt_password",
                    "status",
                    "hypervisor")
                    
            
class OpenvSwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenvSwitch
        fields = (  "owner_Host",
                    "_uuid",
                    "_version",
                    "bridges",
                    "cur_cfg",
                    "db_version",
                    "external_ids",
                    "manager_options",
                    "next_cfg",
                    "other_config",
                    "ovs_version",
                    "ssl",
                    "statistics",
                    "system_type",
                    "system_version")
        
class OVSBridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OVSBridge
        fields = (
                "_uuid",
                "controller",
                "datapath_id",
                "datapath_type",
                "external_ids",
                "fail_mode",
                "flood_vlans",
                "flow_tables",
                "ipfix",
                "mirrors",
                "name",
                "netflow",
                "other_config",
                "ports",
                "protocols",
                "sflow",
                "status",
                "stp_enable")

class OVSPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = OVSPort
        fields = ("_uuid",
            "bond_active_slave",
            "bond_downdelay",
            "bond_fake_iface",
            "bond_mode",
            "bond_updelay",
            "external_ids",
            "fake_bridge",
            "interfaces",
            "lacp",
            "mac",
            "name",
            "other_config",
            "qos",
            "statistics",
            "status",
            "tag",
            "trunks",
            "vlan_mode")
        
class OVSInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OVSInterface
        fields = (  "_uuid",
                    "admin_state",
                    "bfd",
                    "bfd_status",
                    "cfm_fault",
                    "cfm_fault_status",
                    "cfm_flap_count",
                    "cfm_health",
                    "cfm_mpid",
                    "cfm_remote_mpids",
                    "cfm_remote_opstate",
                    "duplex",
                    "external_ids",
                    "link_speed",
                    "link_state",
                    "mac",
                    "mac_in_use",
                    "mtu",
                    "name",
                    "ofport",
                    "ofport_request",
                    "options",
                    "other_config",
                    "statistics")