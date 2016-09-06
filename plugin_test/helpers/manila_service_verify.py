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


from fuelweb_test.helpers import os_actions
from fuelweb_test.settings import SERVTEST_PASSWORD
from fuelweb_test.settings import SERVTEST_TENANT
from fuelweb_test.settings import SERVTEST_USERNAME
from fuelweb_test import logger
from fuelweb_test import logwrap

from helpers import openstack
from helpers import os_manila_actions
from proboscis import asserts


@logwrap
def basic_functionality(openstack_ip=None):
    """This method do basic functionality check :

           * creates share-type, share network, share, access_rule for share;
           * start instance using configuration from server-conf.yaml;
           * mount share  verify R/W to mounted share;

    """

    # init os API client
    os_conn = os_actions.OpenStackActions(openstack_ip, SERVTEST_USERNAME,
                                          SERVTEST_PASSWORD, SERVTEST_TENANT)
    # init manila API client
    manila_conn = os_manila_actions.ManilaActions(openstack_ip,
                                                  SERVTEST_USERNAME,
                                                  SERVTEST_PASSWORD,
                                                  SERVTEST_TENANT)

    # create default share type
    # cli:manila type-create default_share_type True
    manila_conn.create_share_type(type_name='default_share_type')

    # get internal id of admin_internal_net network and subnet id
    # neutron net-list | grep  'admin_internal_net'
    network = os_conn.get_network('admin_internal_net')

    # create share network (share network = internal_admin_network)
    s_net = manila_conn.create_share_network(net_id=network.get('id'),
                                             subnet_id=network.get('subnets'))
    share_network_id = s_net.id

    # create share and wait until it will becomes available
    test_share = manila_conn.create_basic_share(share_name='test_share',
                                                network=share_network_id)

    manila_conn.wait_for_share_status(share_name='test_share',
                                      status='available')
    logger.info('basic Share created and become available')

    # add access rule allow any ip for created share
    manila_conn.add_acc_rule(share_id=test_share, rule='0.0.0.0/0')

    # create and configure instance to verify share
    server_name = openstack.get_defaults()['server']['name']
    test_instance = openstack.create_instance(os_conn)
    openstack.verify_instance_state(os_conn, server_name)

    # assign floating ip for server and wait until it will be avaliable
    fl_ip = openstack.create_and_assign_floating_ips(os_conn, test_instance)

    username = 'manila'
    password = 'manila'
    msg = "IP: {0} user: {1} pass:{2}".format(fl_ip, username, password)
    logger.info(msg)

    ssh_client = openstack.get_ssh_connection(fl_ip, username, password)
    msg = 'New instance started floating ip is: {0}'.format(fl_ip)
    logger.info(msg)

    # create mounting point
    mounting_point = '/mnt/share1'
    cmd = "sudo mkdir {0}".format(mounting_point)
    openstack.execute(ssh_client, cmd)

    # mounting point
    cmd2 = "sudo mount -t nfs {1} {0}".format(mounting_point,
                                              test_share.export_location)
    openstack.execute(ssh_client, cmd2)

    cmd3 = "echo Share is created > {0}/file.txt ".format(mounting_point)
    openstack.execute(ssh_client, cmd3)

    cmd3 = "cat /mnt/share1/file.txt ".format(mounting_point)
    output = openstack.execute(ssh_client, cmd3)
    asserts.assert_true(
        'Share is created' in output['stdout'],
        "R/W access to share {0} verified".format(test_share.export_location))
    logger.info('Network share mounted and work as expected')
