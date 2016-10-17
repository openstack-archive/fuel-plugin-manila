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
from fuelweb_test import logger
from fuelweb_test.settings import SERVTEST_PASSWORD
from fuelweb_test.settings import SERVTEST_TENANT
from fuelweb_test.settings import SERVTEST_USERNAME

from helpers import openstack
from helpers import os_manila_actions
from proboscis import asserts


class TestPluginCheck(object):
    """Test suite for GCS plugin check."""

    def __init__(self, obj):
        # type: (object) -> object
        """Create Test client for run tests.

        :param obj: Test case object
        """

        self.obj = obj
        cluster_id = self.obj.fuel_web.get_last_created_cluster()
        logger.info('#' * 10 + "Cluster ID:  " + str(cluster_id))
        ip = self.obj.fuel_web.get_public_vip(cluster_id)
        logger.info('#' * 10 + "IP :  " + str(ip))

        self.os_conn = os_actions.OpenStackActions(
            ip, SERVTEST_USERNAME, SERVTEST_PASSWORD, SERVTEST_TENANT)

        self.manila_conn = os_manila_actions.ManilaActions(
            ip, SERVTEST_USERNAME, SERVTEST_PASSWORD, SERVTEST_TENANT)

    def verify_share_mount(self, ssh_client, test_share, share_prot):
        # create mounting point
        logger.info('#' * 10 + "Testing share protocol is :  " + share_prot)
        mounting_point = '/mnt/share1'
        cmd = "sudo mkdir {0}".format(mounting_point)
        logger.info('#' * 10 + "Executing :" + cmd)
        openstack.execute(ssh_client, cmd)
        # mounting share
        cmd2 = "sudo mount -t " + share_prot + ' {1} {0}'.format(mounting_point,
            test_share.export_location)
        logger.info('#' * 10 + "Executing :" + cmd2)
        output_1 = openstack.execute(ssh_client, cmd2)
        asserts.assert_true(output_1['exit_code'] == 0,
                            message="Failed to mount network share")
        # create file on share
        cmd3 = "echo Share is created|sudo tee --append {0}/file.txt".\
            format(mounting_point)
        logger.info('#' * 10 + "Executing :" + cmd3)
        output_1 = openstack.execute(ssh_client, cmd3)
        asserts.assert_true(output_1['exit_code'] == 0,
                            message="Failed to create file on network share")
        # read created file
        cmd4 = "cat /mnt/share1/file.txt ".format(mounting_point)
        logger.info('#' * 10 + "Executing :" + cmd4)
        output_2 = openstack.execute(ssh_client, cmd4)
        asserts.assert_true(
            'Share is created' in output_2['stdout'],
            "R/W access for {0} verified".format(test_share.export_location))
        logger.info('#' * 10 + "Network share mounted and work as expected")

    def verify_manila_functionality(self, share_prot='nfs', clean_up=True,
                                    backend='generic'):
        """This method do basic functionality check :

               * creates share-type, share network, share, access_rule ;
               * start instance using configuration from server-conf.yaml;
               * mount share  verify R/W to mounted share;
        """

        # create default share type
        # cli:manila type-create default_share_type True
        logger.info('#'*10 + "Create manila default share type" + '#'*10)
        share_type = self.manila_conn.create_share_type(
            type_name='default_share_type')
        asserts.assert_equal(share_type.name, 'default_share_type',
                             message="Failed to create default share type")
        self.manila_conn.set_share_type_extrascpecs(
            share_type.name,
            {'share_backend_name': backend}
        )

        logger.info('#'*10 + "share type id : " + str(share_type.id))
        # get internal id of admin_internal_net network and subnet id
        # neutron net-list | grep  'admin_internal_net'
        network = self.os_conn.get_network('admin_internal_net')
        logger.debug('admin_internal_net id is :{}'.format(network))

        # create share network (share network = internal_admin_network)
        logger.info('#'*10 + "Create manila share network" + '#' * 10)
        s_net = self.manila_conn.create_share_network(
            net_id=network.get('id'), subnet_id=network.get('subnets'))
        logger.info('#' * 10 + "share type id : " + str(s_net.name))
        asserts.assert_equal(s_net.name, 'test_share_network',
                             message="Failed to create manila share network")

        share_network_id = s_net.id
        logger.info('#'*10 + "Manila share network ID :{0}".format(s_net.id))

        # create share and wait until it will becomes available
        logger.info('#'*10 + "Create manila share" + '#' * 10)
        test_share = self.manila_conn.create_basic_share(
            protocol=share_prot,
            share_name='test_share', network=share_network_id)
        asserts.assert_equal(test_share.name, 'test_share',
                             message="Failed to create manila share")
        self.manila_conn.wait_for_share_status(
            share_name='test_share', status='available')
        logger.info('#'*10 + "Share created and become available")

        logger.info('#'*10 + "add access rule allow any ip for created share")
        self.manila_conn.add_acc_rule(share_id=test_share, rule='0.0.0.0/0')

        logger.info('#'*10 + "Create and configure instance to verify share")
        test_instance, sec_group = openstack.create_instance(self.os_conn)
        openstack.verify_instance_state(self.os_conn, 'test_share_server')

        logger.info('#'*10 + "Assign floating ip for server")
        fl_ip = openstack.create_and_assign_floating_ips(
            self.os_conn, test_instance)
        logger.info("IP: {0} user: {1} pass:{1}".format(fl_ip, 'manila'))

        logger.info('#'*10 + "Connect via ssh to server")
        ssh_client = openstack.get_ssh_connection(fl_ip)

        msg = 'New instance started floating ip is: {0}'.format(fl_ip)
        logger.info(msg)

        self.verify_share_mount(ssh_client, test_share, share_prot)

        if clean_up:
            logger.info('#'*10 + "Cleanup test objects" + '#'*10)
            logger.info('#' * 10 + "Delete test instance")
            openstack.delete_instance(self.os_conn, test_instance)
            logger.info('#' * 10 + "Delete test security group")
            openstack.delete_sec_group(self.os_conn, sec_group.id)

            logger.info('#' * 10 + "Delete test share")
            self.manila_conn.delete_all_shares()
            logger.info('#' * 10 + "Delete test share network")
            self.manila_conn.delete_all_share_networks()
            logger.info('#' * 10 + "Delete test share type ")
            self.manila_conn.delete_all_share_types()
