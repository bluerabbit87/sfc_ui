from django.contrib.auth.models import User, Group
from django.shortcuts import render
from rest_framework import viewsets

from sfc.models import SFF, SF, Interface
from sfc.serializers import UserSerializer, GroupSerializer, SFFSerializer, \
    InterfaceSerializer, SFSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SFViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SF.objects.all()
    serializer_class = SFSerializer

class SFFViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SFF.objects.all()
    serializer_class = SFFSerializer
    
class InterfaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer 
    
    