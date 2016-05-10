from django.contrib.auth.models import User, Group
from django.http.response import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, permissions, mixins, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from sfc.models import Snippet, service_function_forwarder, \
    service_function, data_plane_locator, service_function_chain, \
    service_function_locator, rendered_service_path,\
    rendered_service_path_hop_locator
from sfc.serializers import GroupSerializer, \
    UserSerializer, SnippetSerializer, \
    service_function_forwarder_Serializer, service_function_Serializer, \
    data_plane_locator_Serializer, service_function_chain_Serializer, \
    service_function_locator_Serializer, rendered_service_path_Serializer, \
    rendered_service_path_hop_locator_Serializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class service_function_forwarder_ViewSet(viewsets.ModelViewSet):
    queryset = service_function_forwarder.objects.all()
    serializer_class = service_function_forwarder_Serializer

class service_function_ViewSet(viewsets.ModelViewSet):
    queryset = service_function.objects.all()
    serializer_class = service_function_Serializer

class data_plane_locator_ViewSet(viewsets.ModelViewSet):
    queryset = data_plane_locator.objects.all()
    serializer_class = data_plane_locator_Serializer
    
class service_function_chain_ViewSet(viewsets.ModelViewSet):
    queryset = service_function_chain.objects.all()
    serializer_class = service_function_chain_Serializer
    
class service_function_locator_ViewSet(viewsets.ModelViewSet):
    queryset = service_function_locator.objects.all()
    serializer_class = service_function_locator_Serializer

class rendered_service_path_ViewSet(viewsets.ModelViewSet):
    queryset = rendered_service_path.objects.all()
    serializer_class = rendered_service_path_Serializer   

class rendered_service_path_hop_locator_ViewSet(viewsets.ModelViewSet):
    queryset = rendered_service_path_hop_locator.objects.all()
    serializer_class = rendered_service_path_hop_locator_Serializer