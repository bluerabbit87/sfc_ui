from __future__ import unicode_literals

from django.db import models
import uuid


# Create your models here.
class SFF(models.Model):
    name        = models.CharField(primary_key=True,max_length=50,unique=True)
    type        = models.CharField(max_length=50)
    mgmtIP      = models.CharField(max_length=50)
    
class SF(models.Model):
    device_id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=50)
    type        = models.CharField(max_length=50)
    mgmtIP      = models.CharField(max_length=50)
    connected_sff = models.ForeignKey(SFF)

class Interface(models.Model):
    device_id   = models.ForeignKey(SF)
    name        = models.CharField(max_length=50)
    type        = models.CharField(max_length=50)
    IP          = models.CharField(max_length=50)
    MAC         = models.CharField(max_length=50)
    
