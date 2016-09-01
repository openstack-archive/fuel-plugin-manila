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
import os
import time
from devops.error import TimeoutError
from devops.helpers.helpers import icmp_ping
from devops.helpers.helpers import wait
from fuelweb_test import logger
from fuelweb_test.helpers.utils import pretty_log
import paramiko
from proboscis.asserts import assert_true
import yaml


# timeouts
BOOT_TIMEOUT = 300


def get_defaults(path='/server_conf1.yaml'):
    """Get default parameters from config.yaml."""
    script_dir = os.path.dirname(__file__)
    with open(script_dir + path) as config:
        defaults = yaml.load(config.read())
        return defaults

# defaults
network = get_defaults()['networks']['name']
image = get_defaults()['image_map']['name']
flavor = get_defaults()['flavor']['name']
instance_name = get_defaults()['server']['name']
instance_creds = (
    get_defaults()['os_credentials']['manila']['user'],
    get_defaults()['os_credentials']['manila']['password'])


def create_instance(os_conn, conf_path='/server_conf1.yaml'):
    """Create instances with nova """

    # load server configration from yaml
    server_name = get_defaults(conf_path)['server']['name']
    net = os_conn.get_network(get_defaults(conf_path)['networks']['name'])
    sec_group = os_conn.create_sec_group_for_ssh()
    image = get_defaults(conf_path)['image_map']['name']

    for fl in os_conn.nova.flavors.list():
        if fl.name == 'manila-service-flavor':
            flavor_id = fl.id

    for im in os_conn.glance.images.list():
        if im.name == image:
            image_id = im.id

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
    return server


def verify_instance_state(os_conn, inst_name=None, expected_state='ACTIVE'):
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
    print ip
    wait(lambda: icmp_ping(ip), timeout=60 * 5, interval=5)
    return ip


def get_ssh_connection(ip, username, user_password, timeout=30, port=22):
    """Get ssh to host.

    :param ip: string, host ip to connect to
    :param username: string, a username to use for authentication
    :param user_password: string, a password to use for authentication
    :param timeout: timeout (in seconds) for the TCP connection
    :param port: host port to connect to
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
                ip, port=port,
                username=username,
                password=user_password,
                timeout=30
                )
    return ssh


def execute(ssh_client, command):
    """Execute command on remote host.

    :param ssh_client: SSHClient to instance
    :param command: type string, command to execute
    """
    channel = ssh_client.get_transport().open_session()
    channel.exec_command(command)
    result = {
        'stdout': [],
        'stderr': [],
        'exit_code': 0
    }
    result['exit_code'] = channel.recv_exit_status()
    result['stdout'] = channel.recv(1024)
    result['stderr'] = channel.recv_stderr(1024)
    return result


def remote_execute_command(instance1_ip, instance2_ip, command, wait=30):
    """Check execute remote command.

    :param instance1_ip: string, instance ip connect from
    :param instance2_ip: string, instance ip connect to
    :param command: string, remote command
    :param wait: integer, time to wait available ip of instances
    """
    with get_ssh_connection(
            instance1_ip, instance_creds[0], instance_creds[1]
    ) as ssh:

        interm_transp = ssh.get_transport()
        try:
            logger.info("Opening channel between VMs {0} and {1}".format(
                instance1_ip, instance2_ip))
            interm_chan = interm_transp.open_channel('direct-tcpip',
                                                     (instance2_ip, 22),
                                                     (instance1_ip, 0))
        except Exception as e:
            message = "{} Wait to update sg rules. Try to open channel again"
            logger.info(message.format(e))
            time.sleep(wait)
            interm_chan = interm_transp.open_channel('direct-tcpip',
                                                     (instance2_ip, 22),
                                                     (instance1_ip, 0))
        transport = paramiko.Transport(interm_chan)
        transport.start_client()
        logger.info("Passing authentication to VM")
        transport.auth_password(
            instance_creds[0], instance_creds[1])
        channel = transport.open_session()
        channel.get_pty()
        channel.fileno()
        channel.exec_command(command)

        result = {
            'stdout': [],
            'stderr': [],
            'exit_code': 0
        }
        logger.debug("Receiving exit_code, stdout, stderr")
        result['exit_code'] = channel.recv_exit_status()
        result['stdout'] = channel.recv(1024)
        result['stderr'] = channel.recv_stderr(1024)
        logger.debug('Command: {}'.format(command))
        logger.debug(pretty_log(result))
        logger.debug("Closing channel")
        channel.close()

        return result
