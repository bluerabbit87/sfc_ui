'''
Created on May 4, 2016

@author: root
'''

from rest_framework import serializers

#from sfc.models import Snippet
from openstack.models import VIM, Port, Hypervisor, Network, Server, Interface


class VIMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VIM
        fields = ('id', 'alias', 'project_domain_id', 'user_domain_name', 'project_name', 'tenant_name','username','password','auth_url','version','status')

class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = ('owner_vim','status', 'binding_host_id', 'name', 'allowed_address_pairs', 'admin_state_up', 'network_id','tenant_id','extra_dhcp_opts',
                  'mac_address','binding_vif_details','binding_vif_type','device_owner','binding_profile','port_security_enabled','binding_vnic_type',
                  'fixed_ips','id','security_groups','device_id')

class HypervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hypervisor        
        fields = ('owner_vim',
                  'id',
                  'status',
                  'service',
                  'vcpus_used',
                  'hypervisor_type',
                  'local_gb_used',
                  'vcpus',
                  'hypervisor_hostname',
                  'memory_mb_used',
                  'memory_mb',
                  'current_workload',
                  'state',
                  'host_ip',
                  'cpu_info',
                  'running_vms',
                  'free_disk_gb',
                  'hypervisor_version',
                  'disk_available_least',
                  'local_gb',
                  'free_ram_mb')
        
class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network        
        fields = ('status',                      
        'subnets',                     
        'name' ,                       
        'provider_physical_network',  
        'router_external',    
        'tenant_id',
        'admin_state_up',
        'provider_network_type',
        'port_security_enabled',
        'shared',
        'mtu',
        'id',
        'provider_segmentation_id')

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server        
        fields = (  "owner_vim",             
                    "addresses",
                    "created",
                    "flavor",
                    "hostId",
                    "id",
                    "image",
                    "key_name",
                    "links",
                    "metadata",
                    "security_groups",
                    "status",
                    "tenant_id",
                    "updated",
                    "user_id")

class InterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interface        
        fields = (  "owner_server",
                    "port_state",               
                    "fixed_ips",                   
                    "mac_addr",
                    "net_id",                      
                    "port_id")