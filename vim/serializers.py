'''
Created on May 4, 2016

@author: root
'''



from rest_framework import serializers

from sfc.models import Snippet
from vim.models import vim, port


class vim_Serializer(serializers.ModelSerializer):
    class Meta:
        model = vim
        fields = ('id', 'alias', 'project_domain_id', 'user_domain_id', 'project_name', 'tenant_name','username','password','auth_url','version','status')

class port_Serializer(serializers.ModelSerializer):
    class Meta:
        model = port
        fields = ('owner_vim','status', 'binding', 'name', 'allowed_address_pairs', 'admin_state_up', 'network_id','tenant_id','extra_dhcp_opts',
                  'mac_address','binding_vif_details','binding_vif_type','device_owner','binding_profile','port_security_enabled','binding',
                  'fixed_ips','id','security_groups','device_id')
      