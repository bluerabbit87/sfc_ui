'''
Created on May 4, 2016

@author: root
'''
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from sfc.models import SFF, SF, Interface


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class SFFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SFF
        fields = ('name','type','mgmtIP')
                
class SFSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SF
        fields = ('device_id', 'name','type','mgmtIP','connected_sff')
        
class InterfaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Interface
        fields = ('device_id', 'name','type','IP')
