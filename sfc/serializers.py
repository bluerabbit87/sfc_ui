'''
Created on May 4, 2016

@author: root
'''



from django.contrib.auth.models import User, Group
from rest_framework import serializers

from sfc.models import LANGUAGE_CHOICES, STYLE_CHOICES
from sfc.models import ServiceFunction, ServiceFunctionChain, FlowClassifier, ServiceFunctionGroup


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ServiceFunctionChainSerializer(serializers.HyperlinkedModelSerializer):
    flow_classifier = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    service_function_groups = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    
    class Meta:
        model = ServiceFunctionChain
        fields = ('id', 'tenant_id','name','description','service_function_groups','flow_classifier','chain_parameters','active')


class ServiceFunctionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceFunction
        fields = ('id', 'tenant_id','name','description','ingress','egress','service_function_parameters','Service_function_groups')    


class ServiceFunctionGroupsSerializer(serializers.HyperlinkedModelSerializer):
    service_functions                             = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    
    class Meta:
        model = ServiceFunctionGroup
        fields = ('id', 'tenant_id','name','description','service_function_chain','service_functions')    


class FlowClassifierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FlowClassifier
        fields = ('id', 
                  'tenant_id',
                  'name',
                  'description',
                  'ethertype',
                  'protocol',
                  'source_port_range_min',
                  'source_port_range_max',
                  'destination_port_range_min',
                  'destination_port_range_max',
                  'source_ip_prefix',
                  'destination_ip_prefix',
                  'logical_source_port',
                  'logical_destination_port',
                  'l7_parameters',
                  'service_function_chain')

