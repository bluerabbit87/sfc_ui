from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser, User
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
import uuid

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ('created',)

    
class service_function(models.Model):
    id              = models.CharField(max_length=50,primary_key=True)
    alias           = models.CharField(max_length=50,default="")
    type            = models.CharField(max_length=50,choices=[("UTM",'Endian'),("IPS",'Suricata'),("LB",'HA-Proxy'),("FW",'IPtables')])
    ip_mgmt_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False,default="")
    nsh_aware       = models.BooleanField(default=False)
    
class service_function_forwarder(models.Model):
    id              = models.CharField(max_length=50,primary_key=True)
    alias           = models.CharField(max_length=50,default=None)
    type            = models.CharField(max_length=50,choices=[("OVS",'Open vSwitch'),("DASAN","DASAN OpenFlow Switch")])
    ip_mgmt_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False,default="")
    data_plane      = models.ManyToManyField(
        service_function,
        through='data_plane_locator',
        through_fields=('service_function_forwarder', 'service_function'),
    )
    
class service_function_chain(models.Model):
    id              = models.CharField(max_length=50,primary_key=True)
    alias           = models.CharField(max_length=50,default=None)
    symmetric               = models.BooleanField(default=False)
    service_functions       = models.ManyToManyField(
        service_function,
        through='service_function_locator',
        through_fields=('service_function_chain', 'service_function'),
    )
   
class data_plane_locator(models.Model):
    service_function = models.ForeignKey(service_function, on_delete=models.CASCADE)
    service_function_forwarder = models.ForeignKey(service_function_forwarder, on_delete=models.CASCADE)
    id              = models.AutoField(primary_key=True,default=None)
    mac             = models.CharField(max_length=20,null=True,blank=True)
    vlan_id         = models.IntegerField()
    transport       = models.CharField(max_length=50,choices=[("mac",'mac'),("vxlan-gpe",'vxlan-gpe'),])
    ip_mgmt_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False,default="")
    nsh_aware       = models.BooleanField(default=False)
 

class service_function_locator(models.Model):
    service_function_chain  = models.ForeignKey(service_function_chain, on_delete=models.CASCADE)
    service_function        = models.ForeignKey(service_function, on_delete=models.CASCADE)
    id                      = models.AutoField(primary_key=True,default=None)
    
class rendered_service_path(models.Model):
    id              = models.CharField(max_length=50,primary_key=True)
    alias           = models.CharField(max_length=50,default=None)
    starting_index  = models.IntegerField()
    service_chain_name = models.ForeignKey(service_function_chain)
    rendered_service_path_hop =  models.ManyToManyField(
        data_plane_locator,
        through='rendered_service_path_hop_locator',
        through_fields=('rendered_service_path', 'data_plane_locator'),
    )
class rendered_service_path_hop_locator(models.Model):
    rendered_service_path   = models.ForeignKey(rendered_service_path, on_delete=models.CASCADE)
    data_plane_locator      = models.ForeignKey(data_plane_locator, on_delete=models.CASCADE)
    id                      = models.AutoField(primary_key=True,default=None)
    hop_number              = models.IntegerField()
    service_index           = models.IntegerField()
    