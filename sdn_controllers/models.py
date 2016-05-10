from __future__ import unicode_literals

from django.db import models

# Create your models here.
# class sdn_controller(models.Model):
#     id                  = models.CharField(max_length=50,primary_key=True)
#     alias               = models.CharField(max_length=50,default="")
#     tenant_name         = models.CharField(max_length=50,default="")
#     version   = models.CharField(max_length=50,choices=[("0.9",'0.9'),("1.0",'1.0'),("1.1","1.1"),("1.2","1.2")])
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
