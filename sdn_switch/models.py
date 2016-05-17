from __future__ import unicode_literals

from django.db import models
from sdn_controllers.models import SDNController
from vim.models import Hypervisor


class Host(models.Model):
    id              = models.AutoField(primary_key=True)
    mgmt_ip         = models.CharField(max_length=50,default="unknown")
    mgmt_port       = models.CharField(max_length=50,default="unknown")
    mgmt_id         = models.CharField(max_length=50,default="unknown")
    mgmt_password   = models.CharField(max_length=50,default="unknown")
    status          = models.CharField(max_length=50,default="unknown")
    hypervisor      = models.ForeignKey(Hypervisor,default="unknown")

class OpenvSwitch(models.Model):
    owner_Host      = models.ForeignKey(Host,default=None)
    _uuid           = models.CharField(primary_key=True,max_length=50)
    _version        = models.CharField(max_length=50,default="unknown")
    bridges         = models.CharField(max_length=50,default="unknown")
    cur_cfg         = models.CharField(max_length=50,default="unknown")
    db_version      = models.CharField(max_length=50,default="unknown")
    external_ids    = models.CharField(max_length=50,default="unknown")
    manager_options = models.CharField(max_length=50,default="unknown")
    next_cfg        = models.CharField(max_length=50,default="unknown")
    other_config    = models.CharField(max_length=50,default="unknown")
    ovs_version     = models.CharField(max_length=50,default="unknown")
    ssl             = models.CharField(max_length=50,default="unknown")
    statistics      = models.CharField(max_length=50,default="unknown")
    system_type     = models.CharField(max_length=50,default="unknown")
    system_version  = models.CharField(max_length=50,default="unknown")

class OVSBridge(models.Model):
    _uuid           = models.CharField(primary_key=True,max_length=50,default="unknown")
    owner_Host      = models.ForeignKey(Host,default=None)
    controller      = models.ForeignKey(SDNController,default=None)
    datapath_id     = models.CharField(max_length=50,default="unknown")
    datapath_type   = models.CharField(max_length=50,default="unknown")
    external_ids    = models.CharField(max_length=50,default="unknown")
    fail_mode       = models.CharField(max_length=50,default="unknown")
    flood_vlans     = models.CharField(max_length=50,default="unknown")
    flow_tables     = models.CharField(max_length=50,default="unknown")
    ipfix           = models.CharField(max_length=50,default="unknown")
    mirrors         = models.CharField(max_length=50,default="unknown")
    name            = models.CharField(max_length=50,default="unknown")
    netflow         = models.CharField(max_length=50,default="unknown")
    other_config    = models.CharField(max_length=50,default="unknown")
    ports           = models.CharField(max_length=50,default="unknown")
    protocols       = models.CharField(max_length=50,default="unknown")
    sflow           = models.CharField(max_length=50,default="unknown")
    status          = models.CharField(max_length=50,default="unknown")
    stp_enable      = models.CharField(max_length=50,default="unknown")


class OVSPort(models.Model):
    _uuid               = models.CharField(primary_key=True,max_length=50,default="unknown")
    owner_Bridge        = models.ForeignKey(OVSBridge,default=None)
    bond_active_slave   = models.CharField(max_length=50,default="unknown")
    bond_downdelay      = models.CharField(max_length=50,default="unknown")
    bond_fake_iface     = models.CharField(max_length=50,default="unknown")
    bond_mode           = models.CharField(max_length=50,default="unknown")
    bond_updelay        = models.CharField(max_length=50,default="unknown")
    external_ids        = models.CharField(max_length=50,default="unknown")
    fake_bridge         = models.CharField(max_length=50,default="unknown")
    interfaces          = models.CharField(max_length=50,default="unknown")
    lacp                = models.CharField(max_length=50,default="unknown")
    mac                 = models.CharField(max_length=50,default="unknown")
    name                = models.CharField(max_length=50,default="unknown")
    other_config        = models.CharField(max_length=50,default="unknown")
    qos                 = models.CharField(max_length=50,default="unknown")
    statistics          = models.CharField(max_length=50,default="unknown")
    status              = models.CharField(max_length=50,default="unknown")
    tag                 = models.CharField(max_length=50,default="unknown")
    trunks              = models.CharField(max_length=50,default="unknown")
    vlan_mode           = models.CharField(max_length=50,default="unknown")

class Controller(models.Model):
    _uuid                   = models.CharField(primary_key=True,max_length=50,default="unknown")
    owner_controller        = models.ForeignKey(SDNController,default=None)
    connection_mode         = models.CharField(max_length=50,default="unknown")
    controller_burst_limit  = models.CharField(max_length=50,default="unknown")
    controller_rate_limit   = models.CharField(max_length=50,default="unknown")
    enable_async_messages   = models.CharField(max_length=50,default="unknown")
    external_ids            = models.CharField(max_length=50,default="unknown")
    inactivity_probe        = models.CharField(max_length=50,default="unknown")
    is_connected            = models.CharField(max_length=50,default="unknown")
    local_gateway           = models.CharField(max_length=50,default="unknown")
    local_ip                = models.CharField(max_length=50,default="unknown")
    local_netmask           = models.CharField(max_length=50,default="unknown")
    max_backoff             = models.CharField(max_length=50,default="unknown")
    other_config            = models.CharField(max_length=50,default="unknown")
    role                    = models.CharField(max_length=50,default="unknown")
    status                  = models.CharField(max_length=50,default="unknown")
    target                  = models.CharField(max_length=50,default="unknown")

class OVSInterface(models.Model):
    _uuid                   = models.CharField(primary_key=True,max_length=50,default="unknown")
    owner_host              = models.ForeignKey(Host,default=None)
    admin_state             = models.CharField(max_length=50,default="unknown")
    bfd                     = models.CharField(max_length=50,default="unknown")
    bfd_status              = models.CharField(max_length=50,default="unknown")
    cfm_fault               = models.CharField(max_length=50,default="unknown")
    cfm_fault_status        = models.CharField(max_length=50,default="unknown")
    cfm_flap_count          = models.CharField(max_length=50,default="unknown")
    cfm_health              = models.CharField(max_length=50,default="unknown")
    cfm_mpid                = models.CharField(max_length=50,default="unknown")
    cfm_remote_mpids        = models.CharField(max_length=50,default="unknown")
    cfm_remote_opstate      = models.CharField(max_length=50,default="unknown")
    duplex                  = models.CharField(max_length=50,default="unknown")
    external_ids            = models.CharField(max_length=50,default="unknown")
    link_speed              = models.CharField(max_length=50,default="unknown")
    link_state              = models.CharField(max_length=50,default="unknown")
    mac                     = models.CharField(max_length=50,default="unknown")
    mac_in_use              = models.CharField(max_length=50,default="unknown")
    mtu                     = models.CharField(max_length=50,default="unknown")
    name                    = models.CharField(max_length=50,default="unknown")
    ofport                  = models.CharField(max_length=50,default="unknown")
    ofport_request          = models.CharField(max_length=50,default="unknown")
    options                 = models.CharField(max_length=50,default="unknown")
    other_config            = models.CharField(max_length=50,default="unknown")
    statistics              = models.CharField(max_length=50,default="unknown")



# class Controller(models.Model):
#     _uuid
#     connection_mode
#     controller_burst_limit
#     controller_rate_limit
#     enable_async_messages
#     external_ids
#     inactivity_probe
#     is_connected
#     local_gateway
#     local_ip
#     local_netmask
#     max_backoff
#     other_config
#     role
#     status
#     target


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

# 
# class Interface(models.Model):
# _uuid
# admin_state
# bfd
# bfd_status
# cfm_fault
# cfm_fault_status
# cfm_flap_count
# cfm_health
# cfm_mpid
# cfm_remote_mpids
# cfm_remote_opstate
# duplex
# external_ids
# link_speed
# link_state
# mac
# mac_in_use
# mtu
# name
# ofport
# ofport_request
# options
# other_config
# statistics

