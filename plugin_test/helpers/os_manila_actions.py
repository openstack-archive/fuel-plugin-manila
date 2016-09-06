#    Copyright 2014 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from fuelweb_test.helpers import common
from fuelweb_test.settings import DISABLE_SSL
from fuelweb_test.settings import PATH_TO_CERT
from fuelweb_test.settings import VERIFY_SSL
from keystoneauth1.session import Session as KeystoneSession
from keystoneclient.auth.identity import v2
from manilaclient.v2 import client
from proboscis.asserts import fail


import time


class ManilaActions(common.Common):
    """Manila client class to operate with Manila API"""

    def __make_auth_url(self, controller_ip):
        if DISABLE_SSL:
            auth_url = 'http://{0}:5000/v2.0'.format(controller_ip)
            path_to_cert = None
            return auth_url, path_to_cert
        else:
            auth_url = 'https://{0}:5000/v2.0'.format(controller_ip)
            path_to_cert = PATH_TO_CERT
            return auth_url, path_to_cert

    def __init__(self, controller_ip, user='admin', passwd='admin',
                 tenant='admin'):
        """Create API client for manila service"""
        super(ManilaActions, self).__init__(controller_ip,
                                               user, passwd,
                                               tenant)

        auth_url, cert_path = self.__make_auth_url(controller_ip)
        auth = v2.Password(auth_url=auth_url, username=user,
                           password=passwd, tenant_name=tenant)

        if not DISABLE_SSL:
            if VERIFY_SSL:
                self.__keystone_ses = KeystoneSession(
                    auth=auth, ca_cert=cert_path)
            else:
                self.__keystone_ses = KeystoneSession(
                    auth=auth, verify=False)
        else:
            self.__keystone_ses = KeystoneSession(
                auth=auth)

    def create_share_network(self,
                             net_id=None,
                             subnet_id=None,
                             name='Test Share network',
                             description='For testing purpose'
                             ):
        """Create share network"""
        manila_client = client.Client('2', session=self.__keystone_ses)
        share_network = manila_client.share_networks.create(
            neutron_net_id=net_id,
            neutron_subnet_id=subnet_id,
            nova_net_id=None,
            name=name,
            description=description
        )

        return share_network

    def get_share_network(self, net_name=None):
        """Get share network by name"""

        manila_client = client.Client('2', session=self.__keystone_ses)
        for network in manila_client.share_networks.list():
            if network.name == net_name:
                return network

    def get_share_type(self, name=None):
        """Get a list of all share types"""
        manila_client = client.Client('2', session=self.__keystone_ses)
        if name is None:
            for share_type in manila_client.share_types.list():
                return share_type
        else:
            for share_type in manila_client.share_types.list():
                if share_type.name == name:
                    return share_type

    def create_share_type(self, type_name='Test_share_type',
                          handle_serv=True,
                          snap_sup=True,
                          public_share=True):

        """Create share type"""
        if self.get_share_type(type_name) is None:
            manila_client = client.Client('2', session=self.__keystone_ses)
            manila_client.share_types.create(
                name=type_name,
                spec_driver_handles_share_servers=handle_serv,
                spec_snapshot_support=snap_sup,
                is_public=public_share
            )
        return self.get_share_type(type_name)

    def get_share(self, share_name):
        """Return object share with specified name"""
        manila_client = client.Client('2', session=self.__keystone_ses)
        for share in manila_client.shares.list():
            if share.name == share_name:
                return share
        return None

    def create_basic_share(self, protocol='NFS',
                           size=1,
                           share_name='Default_test_share',
                           share_type='default_share_type',
                           network=None,
                           public_share=True):

        """Create share"""

        manila_client = client.Client('2', session=self.__keystone_ses)
        share = manila_client.shares.create(
            share_proto=protocol,
            size=size,
            name=share_name,
            share_type=share_type,
            share_network=network,
            is_public=public_share
        )
        return share

    def get_shares_list(self):
        """Get a list of all shares."""
        manila_client = client.Client('2', session=self.__keystone_ses)
        for share in manila_client.shares.list():
            return share.name

    def wait_for_share_status(self, share_name, status, timeout=300):
        """Waits for a share to reach a given status."""

        body = self.get_share(share_name)
        share_status = body.status
        start = int(time.time())

        while share_status != status:
            time.sleep(60)
            body = self.get_share(share_name)
            share_status = body.status

            if share_status == status:
                return

            if int(time.time()) - start >= timeout:
                fail("Share '{0}' didn't get status {1} within the required "
                     "timeout '{2}' seconds".format(share_name, status,
                                                    timeout))

    def add_acc_rule(self, share_id, acc_type='ip', rule=None, acc_level='rw'):
        """Add access rule for specific share"""

        manila_client = client.Client('2', session=self.__keystone_ses)
        manila_client.shares.allow(share=share_id, access_type=acc_type,
                                   access=rule,  access_level=acc_level)
