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

from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.settings import DEPLOYMENT_MODE
from fuelweb_test.settings import DISABLE_SSL
from fuelweb_test.settings import NEUTRON_SEGMENT
from fuelweb_test.tests.base_test_case import SetupEnvironment
from fuelweb_test.tests.base_test_case import TestBasic

from helpers import manila_service_verify
from helpers import plugin
from helpers import settings

from proboscis.asserts import assert_true
from proboscis import test

# Defaults upload path image to master node
path = "/var/www/nailgun/plugins/fuel-plugin-manila-1.0/repositories" \
       "/ubuntu"


@test(groups=['manila_plugin', 'manila_bvt_smoke'])
class TestManilaSmoke(TestBasic):
    """Smoke test suite.

    The goal of smoke testing is to ensure that the most critical features
    of Fuel Manila plugin work  after new build delivery. Smoke tests
    will be used by QA to accept software builds from Development team.

    """

    @test(depends_on=[SetupEnvironment.prepare_slaves_1],
          groups=["manila_install"])
    @log_snapshot_after_test
    def manila_install(self):
        """Check that plugin can be installed.

        Scenario:
            1. Upload plugins to the master node
            2. Install plugin.
            3. Ensure that plugin is installed successfully using cli,
               run command 'fuel plugins list'. Check name, version of plugin.
            4.Create a new environment with following parameters:
                * Compute: hypervisor QEMU
                * Networking: Neutron with VLAN segmentation
                * Storage: Cinder LVM over iSCSI for volumes
                * Additional services: default
            5. Enable Manila plugin for new environment.
            6. Attempt to remove enabled plugin.
                Verify that plugin cannot be removed when it already enabled,
                run command 'fuel plugins'.
            7. Disable  plugin
            8. Remove Plugin Manila
                Verify that plugin is removed, run command 'fuel plugins'.
        Duration: 20 min

        """
        self.env.revert_snapshot("ready_with_1_slaves")

        self.show_step(1)
        self.show_step(2)
        plugin.install_manila_plugin(self.ssh_manager.admin_ip)

        cmd = 'fuel plugins list'
        output = self.ssh_manager.execute_on_remote(
            ip=self.ssh_manager.admin_ip,
            cmd=cmd)['stdout'].pop().split(' ')
        self.show_step(3)
        # check name
        assert_true(
            settings.MANILA_PLUGIN_VERSION in output,
            "Plugin version '{0}' not found.".format(
                settings.MANILA_PLUGIN_VERSION)
        )
        # check version
        assert_true(
            settings.plugin_name in output,
            "Plugin '{0}' is not installed.".format(settings.plugin_name)
        )

        self.show_step(4)
        # Configure new cluster
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT['vlan']
            },
            configure_ssl=not DISABLE_SSL
        )

        self.show_step(5)
        plugin.enable_plugin_manila(
            cluster_id, self.fuel_web)

        self.show_step(6)
        cmd = 'fuel plugins --remove {0}=={1}'.format(
            settings.plugin_name, settings.MANILA_PLUGIN_VERSION)
        output = self.ssh_manager.execute_on_remote(
            ip=self.ssh_manager.admin_ip,
            cmd=cmd,
            assert_ec_equal=[1])['stderr'].pop()
        # check for error message
        msg = "delete plugin which is enabled for some environment"

        assert_true(
            msg in output,
            "Expected error message did not found in output"
        )

        self.show_step(7)
        plugin.disable_plugin_manila(
            cluster_id, self.fuel_web)

        self.show_step(8)

        cmd = 'fuel plugins --remove {0}=={1}'.format(
            settings.plugin_name, settings.MANILA_PLUGIN_VERSION)
        output = self.ssh_manager.execute_on_remote(
            ip=self.ssh_manager.admin_ip,
            cmd=cmd)['stdout'].pop().split(' ')

        assert_true(
            plugin.plugin_name not in output,
            "Plugin '{0}' is not removed".format(settings.plugin_name)
        )

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["manila_smoke"])
    @log_snapshot_after_test
    def manila_smoke(self):
        """Check deployment with Manila plugin and one controller.

        Scenario:
            1. Install plugins to the master node + upload Manila_Image
            2. Create a new environment with following parameters:
                * Compute: QEMU
                * Networking: Neutron with VLAN segmentation
                * Storage: Cinder LVM
                * Additional services: default
            3. Enable and configure Manila plugin.
            4. Add nodes with following roles:
                * Controller
                * Compute + Cinder + Manila-share + Manila-data
                * Compute + Cinder
            5. Verify networks.
            6. Deploy the cluster.
            7. Verify Manila service basic functionality (share create/mount).
        Duration: 2.0 hour

        """
        self.env.revert_snapshot("ready_with_3_slaves")
        self.show_step(1)
        self.show_step(2)
        plugin.install_manila_plugin(self.ssh_manager.admin_ip)

        manila_image = plugin.upload_manila_image(
            self.ssh_manager.admin_ip,
            path
        )

        assert_true(
            manila_image,
            "Upload of manila image to master node fail"
        )

        self.show_step(3)
        # Configure new cluster
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT['vlan']
            },
            configure_ssl=not DISABLE_SSL
        )
        self.show_step(4)
        plugin.enable_plugin_manila(
            cluster_id, self.fuel_web)

        self.show_step(5)
        # Assign role to node
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller'],
             'slave-02': ['compute', 'cinder', 'manila-share', 'manila-data'],
             'slave-03': ['compute', 'cinder']
             }
        )
        self.show_step(8)
        self.fuel_web.verify_network(cluster_id)

        self.show_step(9)
        self.fuel_web.deploy_cluster_wait(cluster_id)
        self.env.make_snapshot("manila_smoke_installed", is_make=True)

        self.show_step(10)

        cluster_id = self.fuel_web.get_last_created_cluster()
        os_ip = self.fuel_web.get_public_vip(cluster_id)
        manila_service_verify.basic_functionality(os_ip)

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["manila_bvt"])
    @log_snapshot_after_test
    def manila_bvt(self):
        """Check deployment with Manila plugin and one controller.

        Scenario:
            1. Install plugins to the master node + upload Manila_Image
            2. Create a new environment with following parameters:
                * Compute: QEMU
                * Networking: Neutron with VLAN segmentation
                * Storage: Cinder LVM
                * Additional services: default
            3. Enable and configure Manila plugin.
            4. Add nodes with following roles:
                * Controller + ceph-osd
                * Controller + ceph-osd
                * Controller + ceph-osd
                * Manila-share + Manila-data
                * Compute
            5. Deploy the cluster.
            6. Run OSTF.
            7. Verify Manila service basic functionality (share create/mount).
        Duration: 2.2 hour

        """
        self.env.revert_snapshot("ready_with_5_slaves")
        self.show_step(1)
        plugin.install_manila_plugin(self.ssh_manager.admin_ip)

        manila_image = plugin.upload_manila_image(
            self.ssh_manager.admin_ip,
            path
        )
        assert_true(
            manila_image,
            "Upload of manila image to master node fail"
        )

        self.show_step(2)
        # Configure new cluster
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT['tun'],
                'volumes_lvm': True,
                'volume_ceph': True,
                "image_ceph": True,
                "ephemeral_ceph": True,
                "objects_ceph": True,
                    },
            configure_ssl=not DISABLE_SSL
        )

        self.show_step(3)
        plugin.enable_plugin_manila(
            cluster_id, self.fuel_web)
        self.show_step(4)
        # Assign role to node
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller', 'ceph-osd'],
             'slave-02': ['controller', 'ceph-osd'],
             'slave-03': ['controller', 'ceph-osd'],
             'slave-04': ['manila-share', 'manila-data'],
             'slave-05': ['compute']
             }
        )

        self.show_step(5)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        self.show_step(6)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id, test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(7)
        cluster_id = self.fuel_web.get_last_created_cluster()
        os_ip = self.fuel_web.get_public_vip(cluster_id)
        manila_service_verify.basic_functionality(os_ip)
        self.env.make_snapshot("manila_bvt_installed", is_make=True)
