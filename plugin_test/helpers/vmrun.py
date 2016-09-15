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

import subprocess
from fuelweb_test import logger
from fuelweb_test.settings import ENV_NAME
from proboscis.asserts import assert_true
import libvirt
import commands
import xmltodict

# defaults
config_str = """  <ConfigEntry id="{0}">
    <objID>{1}</objID>
    {2}
  </ConfigEntry>
</ConfigRoot>"""


class Vmrun(object):
    """Vmrun utilite wrapper."""

    def __init__(
            self, host_type, path_to_vmx_file, host_port=None, host_name=None,
            username=None, password=None, guest_password=None,
            guest_username=None):
        """Create Vmrun object."""
        self.username = username
        self.password = password
        self.path = path_to_vmx_file
        self.host_type = host_type
        self.host_name = host_name
        self.host_port = host_port
        self.guest_password = guest_password
        self.guest_username = guest_username
        super(Vmrun, self).__init__()

    def __create_vrun_command(self):
        """Add to vmrun command AUTHENTICATION-FLAGS."""
        cmd = ['vmrun -T {0}'.format(self.host_type)]
        if self.host_port:
            cmd.append('-P {}'.format(self.host_port))
        if self.host_name:
            cmd.append('-h {}'.format(self.host_name))
        if self.username:
            cmd.append('-u {}'.format(self.username))
            assert_true(self.password is not None)
            cmd.append('-p {}'.format(self.password))
        if self.guest_password:
            cmd.append('-vp {}'.format(self.guest_password))
            assert_true(self.guest_username is not None)
            cmd.append('-gu {}'.format(self.guest_username))
        return cmd

    def __execute(self, command):
        """Execute command.

        :param command: type string
        """
        cmd = self.__create_vrun_command()
        cmd.extend([command, '"'+self.path+'"'])
        command_to_run = ' '.join(cmd)
        logger.info('{}'.format(command_to_run))
        subprocess.check_call(command_to_run, shell=True)

    def start(self):
        """Start a virtual machine"""
        self.__execute('start')

    def stop(self):
        """Stopping a virtual machine"""
        self.__execute('stop')

    def reset(self):
        """Reset a virtual machine"""
        self.__execute('reset')

    def register(self):
        """Register a virtual machine"""

        cmd = self.__create_vrun_command()
        grep = '|grep {0}'.format(self.path.split(" ")[1])
        cmd.extend(['listRegisteredVM', grep])
        command_to_run = ' '.join(cmd)
        # check registered vm's
        if self.path.split(" ")[1] not in commands.getoutput(command_to_run):
            cmd = self.__create_vrun_command()
            cmd.extend(['register', '"'+self.path+'"'])
            command_to_run = ' '.join(cmd)
            logger.info('{}'.format(command_to_run))
            subprocess.check_call(command_to_run, shell=True)

    def register_revert_and_setup(self, snapshot_name):
        """revert  a virtual machine """

        self.set_config()
        self.register()
        cmd = self.__create_vrun_command()
        cmd.extend(['revertToSnapshot', '"'+self.path+'"', snapshot_name])
        command_to_run = ' '.join(cmd)
        logger.info('{}'.format(command_to_run))
        assert_true(commands.getstatusoutput(command_to_run)[0] == 0,
                    'Reverting netapp simulator vm failed')
        self.__set_bridges()

    def set_config(self):
        """check vmInventory config and configure if need """

        # check config file and set permissions
        assert_true(commands.getstatusoutput('ls -ld' + commands.mkarg(
            '/etc/vmware/hostd/vmInventory.xml'))[0] == 0,
                    "couldn't find vmInventory config file")
        assert_true(commands.getstatusoutput('sudo chmod 777' + commands.mkarg(
            '/etc/vmware/hostd/vmInventory.xml'))[0] == 0,
                    "couldn't find vmInventory config file")

        # check config for netapp configuration section
        with open(r'/etc/vmware/hostd/vmInventory.xml') as fd:
            conf = xmltodict.parse(fd.read())
        with open(r'/etc/vmware/hostd/vmInventory.xml') as fd:
            str_conf = fd.read()
        for elem in conf['ConfigRoot']['ConfigEntry']:
            vm_path = '/var/lib/vmware/Shared VMs/netapp/netapp.vmx'
            if elem['vmxCfgPath'] == vm_path:
                return
        # add configuration section for netapp
        obj_id = int(conf['ConfigRoot']['ConfigEntry'][-1]['objID']) + 1
        vm_id = "0" * len(
            str(int(conf['ConfigRoot']['ConfigEntry'][-1]['@id']))) + str(
            int(conf['ConfigRoot']['ConfigEntry'][-1]['@id']) + 1)

        string_config = config_str.format(
            vm_id, obj_id,
            '<vmxCfgPath>/var/lib/vmware/Shared '
            'VMs/netapp/netapp.vmx</vmxCfgPath>')

        str_conf = str_conf.replace('</ConfigRoot>', string_config)
        logger.info('new vmInventory.xml :')
        logger.info(str_conf)
        with open('/etc/vmware/hostd/vmInventory.xml', 'w') as fr:
            fr.write(str_conf)
            fr.close()
        return

    def __set_bridges(self):
        """set bridges for virtual machine """
        # define network names
        conn = libvirt.open("qemu:///system")

        # add bridge for private net
        private_bridge_name = conn.networkLookupByName(
            '{0}_private'.format(ENV_NAME))
        cmd = 'sudo brctl  addif {1} {0}'.format(
            'vmnet4',
            private_bridge_name.bridgeName())
        logger.info('adding bridge for private - {0}'.format(cmd))
        logger.info(commands.getstatusoutput(cmd)[1])

        # add bridge for storage net
        storage_bridge_name = conn.networkLookupByName(
            '{0}_storage'.format(ENV_NAME))
        cmd = 'sudo brctl  addif {1} {0}'.format(
            'vmnet4',
            storage_bridge_name.bridgeName())
        logger.info('adding bridge for storage - {0}'.format(cmd))
        logger.info(commands.getstatusoutput(cmd)[1])

        # add bridge for management net
        management_bridge_name = conn.networkLookupByName(
            '{0}_management'.format(ENV_NAME))
        cmd = 'sudo brctl  addif {1} {0}'.format(
            'vmnet4',
            management_bridge_name.bridgeName())
        logger.info('adding bridge for management - {0}'.format(cmd))
        logger.info(commands.getstatusoutput(cmd)[1])
