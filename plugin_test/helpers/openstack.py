"""Copyright 2016 Mirantis, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

from devops.error import TimeoutError
from devops.helpers.helpers import icmp_ping
from devops.helpers.helpers import wait
from fuelweb_test import logger
import paramiko
from proboscis.asserts import assert_true
import socket

# timeouts
BOOT_TIMEOUT = 300


def create_instance(os_conn,
                    server_name='test_share_server',
                    network='admin_internal_net',
                    image='manila-service-image',
                    flavor='manila-service-flavor',
                    ):
    """Create instances with nova """

    # load server configuration from yaml
    net = os_conn.get_network(network)

    for fl in os_conn.nova.flavors.list():
        if fl.name == flavor:
            flavor_id = fl.id

    for im in os_conn.glance.images.list():
        if im.name == image:
            image_id = im.id

    sec_group = os_conn.create_sec_group_for_ssh()
    # create instance
    server = os_conn.create_server(
                                   name=server_name,
                                   security_groups=[sec_group],
                                   flavor_id=flavor_id,
                                   net_id=net['id'],
                                   availability_zone='nova',
                                   timeout=200,
                                   image=image_id
                                   )
    return server, sec_group


def verify_instance_state(os_conn, inst_name, expected_state='ACTIVE'):
    """Verify that current state of each instance/s is expected.

    :param os_conn: type object, openstack
    :param inst_name: type string, name of created instance
    :param expected_state: type string, expected state of instance
    """
    instances = os_conn.nova.servers.list()
    for instance in instances:
        if instance.name == inst_name:
            try:
                wait(
                    lambda:
                    os_conn.get_instance_detail(instance).status ==
                    expected_state, timeout=BOOT_TIMEOUT)
            except TimeoutError:
                current_state = os_conn.get_instance_detail(instance).status
                assert_true(
                    current_state == expected_state,
                    "Timeout is reached.Current state of Vm {0} is {1}".format(
                        instance.name, current_state)
                )
        return instance


def create_and_assign_floating_ips(os_conn, instance):
    """Create Vms on available hypervisors.

    :param os_conn: type object, openstack
    :param instance: type string, name of  instance
    """
    ip = os_conn.assign_floating_ip(instance).ip
    wait(lambda: icmp_ping(ip), timeout=60 * 5, interval=5)
    return ip


def get_ssh_connection(ip, username='manila', user_password='manila',
                       timeout=30,
                       port=22):
    """Get ssh to host.

    :param ip: string, host ip to connect to
    :param username: string, a username to use for authentication
    :param user_password: string, a password to use for authentication
    :param timeout: timeout (in seconds) for the TCP connection
    :param port: host port to connect to
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wait(lambda: sock.connect_ex((ip, port)) == 0, timeout=60 * 5, interval=5)
    logger.info('#' * 10 + "ssh is avaliable on server")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
                ip, port=port,
                username=username,
                password=user_password,
                timeout=timeout
                )
    return ssh


def execute(ssh_client, command):
    """Execute command on remote host.

    :param ssh_client: SSHClient to instance
    :param command: type string, command to execute
    """
    channel = ssh_client.get_transport().open_session()
    channel.exec_command(command)
    result = {'stdout': [],
              'stderr': [],
              'exit_code': 0
              }
    result['exit_code'] = channel.recv_exit_status()
    result['stdout'] = channel.recv(1024)
    result['stderr'] = channel.recv_stderr(1024)
    return result


def delete_instance(os_conn, test_instance):
    """Delete Instance"""

    os_conn.delete_instance(test_instance)
    wait(lambda: os_conn.is_srv_deleted(test_instance), timeout=200,
         timeout_msg='Instance was not deleted.')


def delete_sec_group(os_conn, sec_group):
    """Delete security group"""
    try:
        os_conn.nova.security_groups.delete(sec_group)
    except Exception as exc:
        logger.info(
            'Security group {0} was not deleted. {1}'.format(
                sec_group, exc))


def delete_float_ip(os_conn, ip):
    """Delete Floating IP"""

    os_conn.delete_instance(ip)
    wait(lambda: os_conn.is_srv_deleted(ip), timeout=200,
         timeout_msg='Floating IP was not deleted.')
