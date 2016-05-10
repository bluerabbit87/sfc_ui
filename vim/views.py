from django.http.response import Http404
from django.shortcuts import render
from html5lib import serializer
import keystoneclient.apiclient.exceptions
from keystoneclient.openstack.common.apiclient.exceptions import HTTPClientError
from neutronclient.v2_0 import client
from novaclient.client import Client
from os import environ as env
from rest_framework import generics, status
from rest_framework import viewsets, mixins
from rest_framework.generics import RetrieveUpdateDestroyAPIView, \
    get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

import keystoneclient.v2_0.client as ksclient
from sfc.serializers import UserSerializer
from vim.models import vim, port
from vim.serializers import vim_Serializer, port_Serializer
from vim.utils import print_ports


class vim_ViewSet(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = vim.objects.all()
    serializer_class = vim_Serializer
    
    def get_credentials(self,data):
        credentials = {}
        credentials['username'] = data.username
        credentials['password'] = data.password
        credentials['auth_url'] = data.auth_url
        credentials['tenant_name'] = data.tenant_name
        return credentials
    
    
    def get_nova_credentials_v2(self,data):
        credentials = {}
        credentials['version'] = '2'
        credentials['username'] = data.username
        credentials['password'] = data.password
        credentials['auth_url'] = data.auth_url
        credentials['tenant_name'] = data.tenant_name
        return credentials    
    
    def update_ports(self,data):
        credentials = self.get_credentials(data)
        neutron = client.Client(**credentials)
        ports = neutron.list_ports()
        print_ports(ports)
        pass

    def update_hypervisors(self):
        pass
    
    def update_instances(self):
        pass
    
    def update_networks(self):
        pass
    
    def update_subnets(self):
        pass
    
    def check_status(self, data):
#         print data.project_name
#         print data["user_domain_id"]
#         print data["tenant_name"]        
#         print data["alias"]
#         print data["version"]
#         print data["auth_url"]
#         print data["password"]
#         print data["username"]
#         print data["id"]
#         print data["project_domain_id"]
        try:
            keystone = ksclient.Client(auth_url=data.auth_url,
                                   username=data.username,
                                   password=data.password,
                                   tenant_name=data.tenant_name)

            print keystone.auth_token
            data.status =  "OK, Authorized"
            
        except keystoneclient.apiclient.exceptions.Unauthorized as detail:
            data.status = detail.message
            print "Unauthorized"
        except keystoneclient.apiclient.exceptions.AuthorizationFailure  as detail:
            data.status = detail.message
            print "AuthorizationFailure "
        except keystoneclient.apiclient.exceptions.BadRequest as detail:
            data.status = detail.message
            print "BadRequest "
        except Exception as detail:
            data.status = detail.message
            print "unknowned error"
        data.save()
        
    def create(self, request, *args, **kwargs):
        print "create"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}
    

    def retrieve(self, request, pk=None):
        print "retrieve"
        vim_environment = get_object_or_404(self.queryset, pk=pk)
        
        self.check_status(vim_environment)
        self.update_ports(vim_environment)
        serializer = self.serializer_class(vim_environment)
        return Response(serializer.data)

#   def list(self, request):
#         print "list"
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data)
       
#     def list(self, request):
#         pass
#
#     def create(self, request):
#         pass
# 
#     def retrieve(self, request, pk=None):
#         pass
# 
#     def update(self, request, pk=None):
#         pass
# 
#     def partial_update(self, request, pk=None):
#         pass
# 
#     def destroy(self, request, pk=None):
#         pass
    
class vim_Detail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = vim.objects.all()
    serializer_class = vim_Serializer
    
    def get_object(self, pk):
        print "get_object"
        try:
            return vim.objects.get(pk=pk)
        except vim.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print "detail get"
        vim = self.get_object(pk)
        serializer = vim_Serializer(vim)
        return Response(serializer.data)
    
    def update(self, request, pk, format=None):
        print "detail update"
        vim = self.get_object(pk)
        serializer = vim_Serializer(vim)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        "detail put"
        vim = self.get_object(pk)
        serializer = vim_Serializer(vim, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        "detail delete"
        vim = self.get_object(pk)
        vim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class port_ViewSet(viewsets.ModelViewSet):
    queryset = port.objects.all()
    serializer_class = port_Serializer
