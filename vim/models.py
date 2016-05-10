from __future__ import unicode_literals

from django.db import models

# Create your models here.
class vim(models.Model):
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
    
class port(models.Model):
    owner_vim                  = models.ForeignKey(vim)
    status                      = models.CharField(max_length=50,default="unknown")
    binding                     = models.CharField(max_length=50,default="unknown")
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
    binding                     = models.CharField(max_length=50,default="unknown")
    fixed_ips                   = models.CharField(max_length=50,default="unknown")
    id                          = models.CharField(primary_key=True,max_length=50,default="unknown")
    security_groups             = models.CharField(max_length=50,default="unknown")
    device_id                   = models.CharField(max_length=50,default="unknown")