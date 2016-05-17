from __future__ import unicode_literals

from django.db import models

# Create your models here.
class VIM(models.Model):
    id                  = models.AutoField(primary_key=True)
    alias               = models.CharField(max_length=50,default="")
    project_domain_id   = models.CharField(max_length=50,default="default")
    user_domain_id      = models.CharField(max_length=50,default="default")
    project_name        = models.CharField(max_length=50,default="admin")
    tenant_name         = models.CharField(max_length=50,default="admin")
    username            = models.CharField(max_length=50)
    password            = models.CharField(max_length=50)
    auth_url            = models.CharField(max_length=50,default="http://192.168.43.3:35357/v2.0")
    version             = models.CharField(max_length=50,default="Kilo",choices=[("Kilo","Kilo"),("Liberty",'Liberty'),("Mitaka",'Mitaka')])
    status              = models.CharField(max_length=100,default="unknown")
    
    project_domain_id   
    user_domain_id      
    project_name        
    tenant_name         
    username            
    password            
    auth_url            
    version             
    status          
    
class Port(models.Model):
    owner_vim                   = models.ForeignKey(VIM)
    status                      = models.CharField(max_length=50,default="unknown")
    binding_host_id             = models.CharField(max_length=50,default="unknown")
    name                        = models.CharField(max_length=50,default="unknown") 
    allowed_address_pairs       = models.CharField(max_length=50,default="unknown")
    admin_state_up              = models.CharField(max_length=50,default="unknown")
    network_id                  = models.CharField(max_length=50,default="unknown")
    tenant_id                   = models.CharField(max_length=50,default="unknown")
    extra_dhcp_opts             = models.CharField(max_length=50,default="unknown")
    mac_address                 = models.CharField(max_length=50,default="unknown")
    binding_vif_details         = models.CharField(max_length=50,default="unknown")
    binding_vif_type            = models.CharField(max_length=50,default="unknown")
    device_owner                = models.CharField(max_length=50,default="unknown")
    binding_profile             = models.CharField(max_length=50,default="unknown")
    port_security_enabled       = models.CharField(max_length=50,default="unknown")
    binding_vnic_type           = models.CharField(max_length=50,default="unknown")
    fixed_ips                   = models.CharField(max_length=50,default="unknown")
    id                          = models.CharField(primary_key=True,max_length=50,default="unknown")
    security_groups             = models.CharField(max_length=50,default="unknown")
    device_id                   = models.CharField(max_length=50,default="unknown")
    
    
class Hypervisor(models.Model):
    owner_vim                   = models.ForeignKey(VIM)
    id                          = models.CharField(primary_key=True,max_length=50,default="unknown")
    status                      = models.CharField(max_length=50,default="unknown")
    service                     = models.CharField(max_length=50,default="unknown")
    vcpus_used                  = models.CharField(max_length=50,default="unknown")
    hypervisor_type             = models.CharField(max_length=50,default="unknown")
    local_gb_used               = models.CharField(max_length=50,default="unknown")
    vcpus                       = models.CharField(max_length=50,default="unknown")
    hypervisor_hostname         = models.CharField(max_length=50,default="unknown")
    memory_mb_used              = models.CharField(max_length=50,default="unknown")
    memory_mb                   = models.CharField(max_length=50,default="unknown")
    current_workload            = models.CharField(max_length=50,default="unknown")   
    state                       = models.CharField(max_length=50,default="unknown")
    host_ip                     = models.CharField(max_length=50,default="unknown")
    cpu_info                    = models.CharField(max_length=50,default="unknown")
    running_vms                 = models.CharField(max_length=50,default="unknown")
    free_disk_gb                = models.CharField(max_length=50,default="unknown")
    hypervisor_version          = models.CharField(max_length=50,default="unknown")
    disk_available_least        = models.CharField(max_length=50,default="unknown")
    local_gb                    = models.CharField(max_length=50,default="unknown")
    free_ram_mb                 = models.CharField(max_length=50,default="unknown")
    
class Network(models.Model):
    owner_vim                   = models.ForeignKey(VIM)
    status                      = models.CharField(max_length=50,default="unknown")         
    subnets                     = models.CharField(max_length=50,default="unknown")         
    name                        = models.CharField(max_length=50,default="unknown")         
    provider_physical_network   = models.CharField(max_length=50,default="unknown",null=True, blank=True)         
    router_external             = models.CharField(max_length=50,default="unknown")         
    tenant_id                   = models.CharField(max_length=50,default="unknown")         
    admin_state_up              = models.CharField(max_length=50,default="unknown")         
    provider_network_type       = models.CharField(max_length=50,default="unknown")         
    port_security_enabled       = models.CharField(max_length=50,default="unknown")         
    shared                      = models.CharField(max_length=50,default="unknown")         
    mtu                         = models.CharField(max_length=50,default="unknown")         
    id                          = models.CharField(primary_key=True,max_length=50,default="unknown")         
    provider_segmentation_id    = models.CharField(max_length=50,default="unknown",null=True, blank=True)

class Server(models.Model):
    owner_vim                   = models.ForeignKey(VIM)
    addresses                   = models.CharField(max_length=50,default="unknown")         
    created                     = models.CharField(max_length=50,default="unknown")         
    flavor                      = models.CharField(max_length=50,default="unknown")         
    hostId                      = models.CharField(max_length=50,default="unknown")         
    id                          = models.CharField(primary_key=True,max_length=50,default="unknown")         
    image                       = models.CharField(max_length=50,default="unknown")         
    key_name                    = models.CharField(max_length=50,default="unknown",null=True, blank=True)         
    links                       = models.CharField(max_length=50,default="unknown")         
    metadata                    = models.CharField(max_length=50,default="unknown")         
    security_groups             = models.CharField(max_length=50,default="unknown")         
    status                      = models.CharField(max_length=50,default="unknown")         
    tenant_id                   = models.CharField(max_length=50,default="unknown")         
    updated                     = models.CharField(max_length=50,default="unknown")         
    user_id                     = models.CharField(max_length=50,default="unknown")   
    
    
    addresses                   = models.CharField(max_length=50,default="unknown")         
    created                     = models.CharField(max_length=50,default="unknown")         
    flavor                      = models.CharField(max_length=50,default="unknown")         
    hostId                      = models.CharField(max_length=50,default="unknown")         
    id                          = models.CharField(primary_key=True,max_length=50,default="unknown")         
    image                       = models.CharField(max_length=50,default="unknown")         
    key_name                    = models.CharField(max_length=50,default="unknown",null=True, blank=True)         
    links                       = models.CharField(max_length=50,default="unknown")         
    metadata                    = models.CharField(max_length=50,default="unknown")         
    security_groups             = models.CharField(max_length=50,default="unknown")         
    status                      = models.CharField(max_length=50,default="unknown")         
    tenant_id                   = models.CharField(max_length=50,default="unknown")         
    updated                     = models.CharField(max_length=50,default="unknown")         
    user_id                     = models.CharField(max_length=50,default="unknown")            
    
class Interface(models.Model):
    owner_server                = models.ForeignKey(Server)
    port_state                  = models.CharField(max_length=50,default="unknown")     
    fixed_ips                   = models.CharField(max_length=50,default="unknown")     
    mac_addr                    = models.CharField(primary_key=True,max_length=50,default="unknown")     
    net_id                      = models.CharField(max_length=50,default="unknown")     
    port_id                     = models.CharField(max_length=50,default="unknown")