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
from fuelweb_test.tests.base_test_case import SetupEnvironment
from fuelweb_test.tests.base_test_case import TestBasic

from helpers.manila_service_verify import TestPluginCheck
from helpers import plugin
from proboscis import test


@test(groups=['manila_failover'])
class TestManilaIntegration(TestBasic):
    """Failover test suite.

    The goal of failover testing is to ensure that Fuel Manila plugin work
    on cluster after node with duplicated role unexpected shutdown or reboot

    """

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["manila_shut_reb_controller"])
    @log_snapshot_after_test
    def manila_shut_reb_controller(self):
        """Check that manila-service works after controllers shutdown/reboot.

        Scenario:
            1. Upload plugins and install.
            2. Create environment :
                * Networking: Neutron with VLAN segmentation
                * Block Storage: LVM
                * Other Storages: default
                * Additional services: disabled
            3. Enable plugin and add nodes with following roles:
                * Controller
                * Controller
                * Controller
                * Compute + Manila-data
                * Cinder + Manila-share
            4. Deploy cluster with plugin.
            5. Shutdown primary controller node.
            6. Run OSTF
            7. Verify Manila service basic functionality (share create/mount).
            8. Reboot other controller node.
            9. Run OSTF.
            10. Verify Manila service basic functionality (share add/mount).
        """

        self.env.revert_snapshot("ready_with_5_slaves")
        self.show_step(1)
        plugin.install_manila_plugin(self.ssh_manager.admin_ip)
        plugin.upload_manila_image(self.ssh_manager.admin_ip)

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={}
        )

        self.show_step(3)
        plugin.enable_plugin_manila(cluster_id, self.fuel_web)
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller'],
             'slave-02': ['controller'],
             'slave-03': ['controller'],
             'slave-04': ['compute', 'manila-share'],
             'slave-05': ['cinder', 'manila-data']
             }
        )

        self.show_step(4)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        cluster_id = self.fuel_web.get_last_created_cluster()

        primary_controller_node = self.fuel_web.get_nailgun_primary_node(
            self.env.d_env.nodes().slaves[0])

        self.show_step(5)
        self.fuel_web.warm_shutdown_nodes([primary_controller_node])

        self.show_step(6)
        self.fuel_web.run_ostf(cluster_id=cluster_id,
                               test_sets=['smoke', 'sanity'])
        self.show_step(7)
        TestPluginCheck(self).verify_manila_functionality()

        self.show_step(8)
        d_contr_2 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-02'))

        self.fuel_web.cold_restart_nodes([d_contr_2])

        self.show_step(9)
        self.fuel_web.run_ostf(cluster_id=cluster_id,
                               test_sets=['smoke', 'sanity'])

        self.show_step(10)
        TestPluginCheck(self).verify_manila_functionality()

