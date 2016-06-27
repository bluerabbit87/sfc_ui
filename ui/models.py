from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    addreq          = models.CharField(max_length=50,default="")
    curalarmseq     = models.CharField(primary_key=True,max_length=50,default="")
    orgnamescode    = models.CharField(max_length=50,default="")
    serveruuid      = models.CharField(max_length=50,default="")
    monitemistancesq= models.CharField(max_length=50,default="")
    perceive_user   = models.CharField(max_length=50,default="")
    resolve_user    = models.CharField(max_length=50,default="")
    
# Create your models here.
