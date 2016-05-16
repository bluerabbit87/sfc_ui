from __future__ import unicode_literals

from django.db import models

from sdn_switch.models import Host
import uuid


class SDNController(models.Model):
    id              = models.AutoField(primary_key=True,default=None)
    mgmt_ip         = models.CharField(max_length=50,default="unknown")
    mgmt_port       = models.CharField(max_length=50,default="unknown")
    status          = models.CharField(max_length=50,default="unknown")
    health          = models.CharField(max_length=50,default="unknown")
    memory          = models.CharField(max_length=50,default="unknown")
    uptime          = models.CharField(max_length=50,default="unknown")
    tables          = models.CharField(max_length=50,default="unknown")
    role            = models.CharField(max_length=50,default="unknown")
    summary         = models.CharField(max_length=50,default="unknown")
    tables          = models.CharField(max_length=50,default="unknown")
    host            = models.ForeignKey(Host)

    
class OpenFlowSwitch(models.Model):
    dpid                    = models.CharField(primary_key=True, max_length=50,default="unknown")
    datapathDescription     = models.CharField(max_length=50,default="unknown")
    hardwareDescription     = models.CharField(max_length=50,default="unknown")
    manufacturerDescription = models.CharField(max_length=50,default="unknown")
    serialNumber            = models.CharField(max_length=50,default="unknown")
    softwareDescription     = models.CharField(max_length=50,default="unknown")
    version                 = models.CharField(max_length=50,default="unknown")

class OpenFlowEntry(models.Model):
    owner_switch            = models.ForeignKey(OpenFlowSwitch)
    byteCount               = models.CharField(max_length=50,default="unknown")
    cookie                  = models.CharField(max_length=50,default="unknown")
    durationNSeconds        = models.CharField(max_length=50,default="unknown")
    durationSeconds         = models.CharField(max_length=50,default="unknown")
    flags                   = models.CharField(max_length=50,default="unknown")
    hardTimeoutSec          = models.CharField(max_length=50,default="unknown")
    idleTimeoutSec          = models.CharField(max_length=50,default="unknown")
    instructions            = models.CharField(max_length=50,default="unknown")
    match                   = models.CharField(max_length=50,default="unknown")
    packetCount             = models.CharField(max_length=50,default="unknown")
    priority                = models.CharField(max_length=50,default="unknown")
    tableId                 = models.CharField(max_length=50,default="unknown")
    version                 = models.CharField(max_length=50,default="unknown")
    
class OpenFlowPort(models.Model):    
    id                      = models.AutoField(primary_key=True,default=None)
    owner_switch            = models.ForeignKey(OpenFlowSwitch)
    version                 = models.CharField(max_length=50,default="unknown")
    collisions              = models.CharField(max_length=50,default="unknown")
    durationNsec            = models.CharField(max_length=50,default="unknown")
    durationSec             = models.CharField(max_length=50,default="unknown")
    portNumber              = models.CharField(max_length=50,default="unknown")
    receiveBytes            = models.CharField(max_length=50,default="unknown")
    receiveCRCErrors        = models.CharField(max_length=50,default="unknown")
    receiveDropped          = models.CharField(max_length=50,default="unknown")
    receiveErrors           = models.CharField(max_length=50,default="unknown")
    receiveFrameErrors      = models.CharField(max_length=50,default="unknown")
    receiveOverrunErrors    = models.CharField(max_length=50,default="unknown")
    receivePackets          = models.CharField(max_length=50,default="unknown")
    transmitBytes           = models.CharField(max_length=50,default="unknown")
    transmitDropped         = models.CharField(max_length=50,default="unknown")
    transmitErrors          = models.CharField(max_length=50,default="unknown")
    transmitPackets         = models.CharField(max_length=50,default="unknown")
