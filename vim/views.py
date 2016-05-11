from django.core.exceptions import ObjectDoesNotExist
from neutronclient.v2_0 import client
from novaclient.client import Client
from rest_framework import status,viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings
from vim.models import VIM, Port, Hypervisor, Network, Server, Interface
from vim.serializers import VIMSerializer, PortSerializer, \
    HypervisorSerializer, NetworkSerializer, ServerSerializer, \
    InterfaceSerializer
from vim.utils import  print_values
import keystoneclient.apiclient.exceptions
import keystoneclient.v2_0.client as ksclient
class VIMViewSet(mixins.ListModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = VIM.objects.all()
    serializer_class = VIMSerializer
    
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
        credentials['api_key'] = data.password
        credentials['auth_url'] = data.auth_url
        credentials['project_id'] = data.tenant_name
        return credentials    
    
    def update_ports(self,data):
        credentials = self.get_credentials(data)
        neutron = client.Client(**credentials)
        ports = neutron.list_ports()
        
        port_list = ports['ports']
        for port in port_list:
            try:
                print "Port is  exist, update ports"
                new_port = Port.objects.get(pk = port["id"])
                new_port.owner_vim                  = data
                new_port.status                     = port["status"]
                new_port.binding_host_id            = port["binding:host_id"]
                new_port.name                        = port["name"]
                new_port.allowed_address_pairs       = port["allowed_address_pairs"]
                new_port.admin_state_up              = port["admin_state_up"]
                new_port.network_id                  = port["network_id"]
                new_port.tenant_id                   = port["tenant_id"]
                new_port.extra_dhcp_opts             = port["extra_dhcp_opts"]
                new_port.mac_address                 = port["mac_address"]
                new_port.binding_vif_details         = port["binding:vif_details"]
                new_port.binding_vif_type            = port["binding:vif_type"]
                new_port.device_owner                = port["device_owner"]
                new_port.binding_profile             = port["binding:profile"]
                new_port.port_security_enabled       = port["port_security_enabled"]
                new_port.binding_vnic_type           = port["binding:vnic_type"]
                new_port.fixed_ips                   = port["fixed_ips"]
                new_port.id                          = port["id"]
                new_port.security_groups             = port["security_groups"]
                new_port.device_id                   = port["device_id"]
                new_port.save()
                
            except ObjectDoesNotExist as detail:
                print "Port is not exist, Add ports"
                new_port = Port (owner_vim                  = data,
                                status                      = port["status"],
                                binding_host_id             = port["binding:host_id"],
                                name                        = port["name"],
                                allowed_address_pairs       = port["allowed_address_pairs"],
                                admin_state_up              = port["admin_state_up"],
                                network_id                  = port["network_id"],
                                tenant_id                   = port["tenant_id"],
                                extra_dhcp_opts             = port["extra_dhcp_opts"],
                                mac_address                 = port["mac_address"],
                                binding_vif_details         = port["binding:vif_details"],
                                binding_vif_type            = port["binding:vif_type"],
                                device_owner                = port["device_owner"],
                                binding_profile             = port["binding:profile"],
                                port_security_enabled       = port["port_security_enabled"],
                                binding_vnic_type           = port["binding:vnic_type"],
                                fixed_ips                   = port["fixed_ips"],
                                id                          = port["id"],
                                security_groups             = port["security_groups"],
                                device_id                   = port["device_id"])
                new_port.save()
                
    
    
    def update_hypervisors(self,data):
        credentials = self.get_nova_credentials_v2(data)
        nova_client = Client(**credentials)
        
        hypervisors = nova_client.hypervisors.list()
        for hypervisor in hypervisors:
            try:
                new_hypervisor = Hypervisor.objects.get(pk = hypervisor.id)
                print "The Hypervisor is exist, update the Hypervisor"
                new_hypervisor.id = hypervisor.id
                new_hypervisor.status = hypervisor.status
                new_hypervisor.service = hypervisor.service
                new_hypervisor.vcpus_used = hypervisor.vcpus_used
                new_hypervisor.hypervisor_type = hypervisor.hypervisor_type
                new_hypervisor.local_gb_used = hypervisor.local_gb_used
                new_hypervisor.vcpus = hypervisor.vcpus
                new_hypervisor.hypervisor_hostname = hypervisor.hypervisor_hostname
                new_hypervisor.memory_mb_used = hypervisor.memory_mb_used
                new_hypervisor.memory_mb = hypervisor.memory_mb
                new_hypervisor.current_workload = hypervisor.current_workload
                new_hypervisor.state= hypervisor.state
                new_hypervisor.host_ip = hypervisor.host_ip
                new_hypervisor.cpu_info= hypervisor.cpu_info
                new_hypervisor.running_vms = hypervisor.running_vms
                new_hypervisor.free_disk_gb = hypervisor.free_disk_gb
                new_hypervisor.hypervisor_version = hypervisor.hypervisor_version
                new_hypervisor.disk_available_least = hypervisor.disk_available_least
                new_hypervisor.local_gb = hypervisor.local_gb
                new_hypervisor.free_ram_mb = hypervisor.free_ram_mb
                new_hypervisor.save()
            except ObjectDoesNotExist as detail:
                print "The hypervisor is not exist, Add the hypervisor"
                new_Hypervisor = Hypervisor (
                                            owner_vim = data,
                                            id = hypervisor.id,
                                            status = hypervisor.status,
                                            service = hypervisor.service,
                                            vcpus_used = hypervisor.vcpus_used,
                                            hypervisor_type = hypervisor.hypervisor_type,
                                            local_gb_used = hypervisor.local_gb_used,
                                            vcpus = hypervisor.vcpus,
                                            hypervisor_hostname = hypervisor.hypervisor_hostname,
                                            memory_mb_used = hypervisor.memory_mb_used,
                                            memory_mb = hypervisor.memory_mb,
                                            current_workload = hypervisor.current_workload,
                                            state= hypervisor.state,
                                            host_ip = hypervisor.host_ip,
                                            cpu_info= hypervisor.cpu_info,
                                            running_vms = hypervisor.running_vms,
                                            free_disk_gb = hypervisor.free_disk_gb,
                                            hypervisor_version = hypervisor.hypervisor_version,
                                            disk_available_least = hypervisor.disk_available_least,
                                            local_gb = hypervisor.local_gb,
                                            free_ram_mb = hypervisor.free_ram_mb)
                new_Hypervisor.save()
                
    def update_instances(self,data):
        print "update_instances"
        credentials = self.get_nova_credentials_v2(data)
        nova_client = Client(**credentials)
        servers = nova_client.servers.list()
        for server in servers:
            new_server = None
            try:
                print "Update server"
                new_server              = Server.objects.get(pk = server.id)
                new_server.addresses    = server.addresses
                new_server.created      = server.created 
                new_server.flavor       = server.flavor 
                new_server.hostId       = server.hostId 
                new_server.image        = server.image 
                new_server.key_name     = server.key_name 
                new_server.links        = server.links 
                new_server.metadata     = server.metadata 
                new_server.security_groups  = server.security_groups 
                new_server.status       = server.status 
                new_server.tenant_id    = server.tenant_id 
                new_server.updated      = server.updated 
                new_server.user_id      = server.user_id 
                new_server.save()
            except ObjectDoesNotExist as detail:
                print type(detail)
                print "Add the server"
                new_server      = Server(
                                        owner_vim = data,
                                        id           = server.id,
                                        addresses    = server.addresses,
                                        created      = server.created,
                                        flavor       = server.flavor,
                                        hostId       = server.hostId, 
                                        image        = server.image, 
                                        key_name     = server.key_name, 
                                        links        = server.links, 
                                        metadata     = server.metadata, 
                                        security_groups  = server.security_groups, 
                                        status       = server.status, 
                                        tenant_id    = server.tenant_id, 
                                        updated      = server.updated, 
                                        user_id      = server.user_id)
                new_server.save()
              
            interfaces = server.interface_list()
            for interface in interfaces:
                try:
                    print "Update interface"
                 
                    new_interface               = Interface.objects.get(pk = interface.mac_addr)
                    new_interface.owner_server  = new_server
                    new_interface.port_state    = interface.port_state
                    new_interface.fixed_ips     = interface.fixed_ips
                    #new_interface.mac_addr      = interface.mac_addr
                    new_interface.net_id        = interface.net_id
                    new_interface.port_id       = interface.port_id
                    new_interface.save()
                     
                except ObjectDoesNotExist as detail:
                    print "Add interface"
                    new_interface               = Interface(
                                                    owner_server  = new_server,
                                                    port_state    = interface.port_state,
                                                    fixed_ips     = interface.fixed_ips,
                                                    mac_addr      = interface.mac_addr,
                                                    net_id        = interface.net_id,
                                                    port_id       = interface.port_id)
                    new_interface.save()
            
    def update_interfaces(self,data,interfaces):
        pass

    
    def update_networks(self,data):
        credentials = self.get_credentials(data)
        neutron = client.Client(**credentials)
        netw = neutron.list_networks()
        print_values(netw, 'networks')
        network_list = netw['networks']
        new_network = []
        for network in network_list:
            try:
                print "network is  exist, network ports"
                new_network = Network.objects.get(pk = network["id"])
                new_network.owner_vim   = data
                new_network.status      = network['status']
                new_network.subnets     = network['subnets']
                new_network.name        = network['name']
                new_network.provider_physical_network = network[u'provider:physical_network']
                new_network.router_external = network[u'router:external']
                new_network.tenant_id       = network['tenant_id']
                new_network.admin_state_up  = network['admin_state_up']
                new_network.provider_network_type = network[u'provider:network_type']
                new_network.port_security_enabled = network['port_security_enabled']
                new_network.shared          = network['shared']
                new_network.mtu             = network['mtu']
                new_network.provider_segmentation_id = network[u'provider:segmentation_id']
                new_network.save()
                
            except ObjectDoesNotExist as detail:
                print "network is not exist, Add network"
                new_network = Network (owner_vim                  = data,
                                id                        = network['id'],
                                status      = network['status'],
                                subnets     = network['subnets'],
                                name        = network['name'],
                                provider_physical_network = network[u'provider:physical_network'],
                                router_external = network[u'router:external'],
                                tenant_id       = network['tenant_id'],
                                admin_state_up  = network['admin_state_up'],
                                provider_network_type = network[u'provider:network_type'],
                                port_security_enabled = network['port_security_enabled'],
                                shared          = network['shared'],
                                mtu             = network['mtu'],
                                provider_segmentation_id = network[u'provider:segmentation_id']
                                )
                new_network.save()
#             print network.keys()
#             print network['status']
#             print network['subnets']
#             print network['name']
#             print network[u'provider:physical_network']
#             print network[u'router:external']
#             print network['tenant_id']
#             print network['admin_state_up']
#             print network[u'provider:network_type']
#             print network['port_security_enabled']
#             print network['shared']
#             print network['mtu']
#             print network['id']
#             print network[u'provider:segmentation_id']
           

            
#         owner_vim                   = models.ForeignKey(VIM)
#         status                      = models.CharField(max_length=50,default="unknown")         
#         subnets                     = models.CharField(max_length=50,default="unknown")         
#         name                        = models.CharField(max_length=50,default="unknown")         
#         provider_physical_network   = models.CharField(max_length=50,default="unknown")         
#         router_external             = models.CharField(max_length=50,default="unknown")         
#         tenant_id                   = models.CharField(max_length=50,default="unknown")         
#         admin_state_up              = models.CharField(max_length=50,default="unknown")         
#         provider_network_type       = models.CharField(max_length=50,default="unknown")         
#         port_security_enabled       = models.CharField(max_length=50,default="unknown")         
#         shared                      = models.CharField(max_length=50,default="unknown")         
#         mtu                         = models.CharField(max_length=50,default="unknown")         
#         id                          = models.CharField(primary_key=True,max_length=50,default="unknown")         
#         provider_segmentation_id    = models.CharField(max_length=50,default="unknown")
        pass
    
    def update_subnets(self):
        pass
    
    def check_status(self, data):
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
        #self.update_ports(vim_environment)
        #self.update_hypervisors(vim_environment)
        self.update_networks(vim_environment)
        #self.update_instances(vim_environment)
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
    
# class vim_Detail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     
#     queryset = vim.objects.all()
#     serializer_class = vim_Serializer
#     
#     def get_object(self, pk):
#         print "get_object"
#         try:
#             return vim.objects.get(pk=pk)
#         except vim.DoesNotExist:
#             raise Http404
# 
#     def get(self, request, pk, format=None):
#         print "detail get"
#         vim = self.get_object(pk)
#         serializer = vim_Serializer(vim)
#         return Response(serializer.data)
#     
#     def update(self, request, pk, format=None):
#         print "detail update"
#         vim = self.get_object(pk)
#         serializer = vim_Serializer(vim)
#         return Response(serializer.data)
# 
#     def put(self, request, pk, format=None):
#         "detail put"
#         vim = self.get_object(pk)
#         serializer = vim_Serializer(vim, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 
#     def delete(self, request, pk, format=None):
#         "detail delete"
#         vim = self.get_object(pk)
#         vim.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
class PortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer
    
class HypervisorViewSet(viewsets.ModelViewSet):
    queryset = Hypervisor.objects.all()
    serializer_class = HypervisorSerializer

class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    
class InterfaceViewSet(viewsets.ModelViewSet):
    queryset = Interface.objects.all()
    serializer_class = InterfaceSerializer
