from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
import uuid

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class ServiceFunctionChain(models.Model):
    id              = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    tenant_id       = models.UUIDField()
    name            = models.CharField(max_length=200,default="")
    description     = models.CharField(max_length=200,default="")
    flow_classifiers  = models.CharField(max_length=200,default="")
    chain_parameters  = models.CharField(max_length=200,null=True, blank=True)
    active            = models.CharField(max_length=50,default="inactive",choices=[("inactive","inactive"),("active",'active')])

class FlowClassifier(models.Model):
    id              = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    tenant_id       = models.UUIDField()
    name            = models.CharField(max_length=50,default="")
    description     = models.CharField(max_length=50,default="")
    ethertype       = models.CharField(max_length=50,null=True, blank=True)    
    protocol        = models.CharField(max_length=50,null=True, blank=True)
    source_port_range_min   = models.CharField(max_length=50,null=True, blank=True)
    source_port_range_max   = models.CharField(max_length=50,null=True, blank=True)
    destination_port_range_min  = models.CharField(max_length=50,null=True, blank=True)
    destination_port_range_max  = models.CharField(max_length=50,null=True, blank=True)
    source_ip_prefix            = models.CharField(max_length=50,null=True, blank=True)
    destination_ip_prefix       = models.CharField(max_length=50,null=True, blank=True)
    logical_source_port         = models.UUIDField(null=True, blank=True)
    logical_destination_port    = models.UUIDField(null=True, blank=True)
    l7_parameters               = models.CharField(max_length=50,null=True, blank=True)
    service_function_chain      = models.ForeignKey(ServiceFunctionChain,null=True, blank=True, related_name='flow_classifier')

class ServiceFunctionGroup(models.Model):
    id              = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    tenant_id       = models.UUIDField()
    name            = models.CharField(max_length=50,default="")
    description     = models.CharField(max_length=50,default="")
    service_function_chain = models.ForeignKey(ServiceFunctionChain,null=True, blank=True, related_name='service_function_groups')
    
class ServiceFunction(models.Model):
    id              = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    tenant_id       = models.UUIDField()
    name            = models.CharField(max_length=50,default="")
    description     = models.CharField(max_length=50,default="")
    ingress         = models.UUIDField(max_length=200)
    egress          = models.UUIDField(max_length=200)
    service_function_parameters = models.CharField(max_length=200,default="")
    Service_function_groups     = models.ForeignKey(ServiceFunctionGroup,null=True, blank=True, related_name='service_functions')
    