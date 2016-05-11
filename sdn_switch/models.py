from __future__ import unicode_literals

from django.db import models
from vim.models import Hypervisor

class OpenvSwitch(models.Model):
    owner_hypervisor = models.ForeignKey(Hypervisor)
    root_password    = models.CharField(max_length=50,default="unknown")
    root_id          = models.CharField(max_length=50,default="unknown")
    status           = models.CharField(max_length=50,default="unknown")
    _uuid            = models.CharField(max_length=50,default="unknown")
    bridges          = models.CharField(max_length=50,default="unknown")
    cur_cfg          = models.CharField(max_length=50,default="unknown")
    db_version       = models.CharField(max_length=50,default="unknown")
    external_ids     = models.CharField(max_length=50,default="unknown")
    manager_options  = models.CharField(max_length=50,default="unknown")
    next_cfg         = models.CharField(max_length=50,default="unknown")
    other_config     = models.CharField(max_length=50,default="unknown")
    ovs_version      = models.CharField(max_length=50,default="unknown")
    ssl              = models.CharField(max_length=50,default="unknown")
    statistics       = models.CharField(max_length=50,default="unknown")
    system_type      = models.CharField(max_length=50,default="unknown")
    system_version   = models.CharField(max_length=50,default="unknown")




# Create your models here.
# class Bridge(models.Model):
#     _uuid
#     controller
#     datapath_id
#     datapath_type
#     external_ids
#     fail_mode
#     flood_vlans
#     flow_tables
#     ipfix
#     mirrors
#     name
#     netflow
#     other_config
#     ports
#     protocols
#     sflow
#     status
#     stp_enable
# 
# 
# class Port(models.Model):
#     _uuid
#     bond_active_slave
#     bond_downdelay
#     bond_fake_iface
#     bond_mode
#     bond_updelay
#     external_ids
#     fake_bridge
#     interfaces
#     lacp
#     mac
#     name
#     other_config
#     qos
#     statistics
#     status
#     tag
#     trunks
#     vlan_mode
# 
# class Open_vSwitch(models.Model):
#     _uuid
#     bridges
#     cur_cfg
#     db_version
#     external_ids
#     manager_options
#     next_cfg
#     other_config
#     ovs_version
#     ssl
#     statistics
#     system_type
#     system_version
# 
# class Open_vSwitch(models.Model):
#     _uuid
#     controller
#     datapath_id
#     datapath_type
#     external_ids
#     fail_mode
#     flood_vlans
#     flow_tables
#     ipfix
#     mirrors
#     name
#     netflow
#     other_config
#     ports
#     protocols
#     sflow
#     status
#     stp_enable

