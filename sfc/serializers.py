'''
Created on May 4, 2016

@author: root
'''



from django.contrib.auth.models import User, Group
from rest_framework import serializers

from sfc.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, \
    data_plane_locator, service_function_chain, service_function_locator, \
    rendered_service_path, rendered_service_path_hop_locator
from sfc.models import service_function_forwarder, service_function


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class service_function_Serializer(serializers.ModelSerializer):
    class Meta:
        model = service_function
        fields = ('id', 'alias','type','ip_mgmt_address','nsh_aware')    
        
class service_function_forwarder_Serializer(serializers.ModelSerializer):
    class Meta:
        model = service_function_forwarder
        fields = ('id', 'alias','type','ip_mgmt_address','data_plane')

    
class data_plane_locator_Serializer(serializers.ModelSerializer):
    class Meta:
        model = data_plane_locator
        fields = ('service_function', 'service_function_forwarder','id','mac','vlan_id','transport','ip_mgmt_address','nsh_aware')  


class service_function_chain_Serializer(serializers.ModelSerializer):
    class Meta:
        model = service_function_chain
        fields = ('id', 'symmetric','service_functions')
        
class service_function_locator_Serializer(serializers.ModelSerializer):
    class Meta:
        model = service_function_locator
        fields = ('service_function_chain','service_function','id')  
        
class rendered_service_path_Serializer(serializers.ModelSerializer):
    class Meta:
        model = rendered_service_path
        fields = ('id', 'alias','starting_index','service_chain_name','rendered_service_path_hop')        

class rendered_service_path_hop_locator_Serializer(serializers.ModelSerializer):
    class Meta:
        model = rendered_service_path_hop_locator
        fields = ('rendered_service_path', 'data_plane_locator','id','hop_number','service_index')        
    

