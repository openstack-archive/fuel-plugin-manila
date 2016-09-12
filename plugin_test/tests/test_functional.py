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
from fuelweb_test.tests.base_test_case import SetupEnvironment
from fuelweb_test.tests.base_test_case import TestBasic

from helpers.manila_service_verify import TestPluginCheck
from helpers import plugin
from proboscis import test


@test(groups=['manila_plugin', 'manila_integration'])
class TestManilaFunctional(TestBasic):
    """Functional test suite.

    The goal of functional testing is to ensure that Fuel Manila plugin work
    after reconfiguring cluster and redeploy (adding and removing nodes with
    core roles (controller, compute, cinder, ceph-osd, manila-data,
    manila-share)

    """

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["manila_del_add_controller"])
    @log_snapshot_after_test
    def manila_del_add_controller(self):
        """Check deploy with Manila Plugin after controller remove and add.

        Scenario:
            1. Upload plugins and install.
            2. Create environment :
                * Networking: Neutron with VLAN segmentation
                * Block Storage: LVM
                * Other Storages: default
                * Additional services: disabled
            3. Enable plugin and add nodes with following roles:
                * Controller + Manila-share
                * Controller + Manila-data
                * Controller
                * Cinder
                * Compute
            4. Deploy cluster with plugin.
            5. Run OSTF
            6. Verify Manila service basic functionality (share create/mount).
            7. Delete node with controller role
            8. Deploy changes
            9. Run OSTF
            10. Verify Manila service basic functionality (share create/mount).
            11. Add a node with controller role
            12. Deploy changes
            13. Run OSTF
            14. Verify Manila service basic functionality (share create/mount).

        """

        self.env.revert_snapshot("ready_with_5_slaves")
        self.show_step(1)
        plugin.install_manila_plugin(self.ssh_manager.admin_ip)
        plugin.upload_manila_image(self.ssh_manager.admin_ip)

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                'volumes_ceph': False,
                'volumes_lvm': False
            }
        )

        self.show_step(3)
        plugin.enable_plugin_manila(cluster_id, self.fuel_web)
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller', 'manila-share'],
             'slave-02': ['controller', 'manila-data'],
             'slave-03': ['controller'],
             'slave-04': ['cinder'],
             'slave-05': ['compute']
             }
        )

        self.show_step(4)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        self.show_step(5)
        self.fuel_web.run_ostf(cluster_id=cluster_id,
                               test_sets=['smoke', 'sanity'])

        self.show_step(6)
        TestPluginCheck(self).verify_manila_functionality()

        self.show_step(7)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-01': ['controller']},
            pending_addition=False, pending_deletion=True)

        self.show_step(8)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )

        self.show_step(9)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=0,
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(10)
        TestPluginCheck(self).plugin_check()

        self.show_step(11)
        self.fuel_web.update_nodes(
            cluster_id, {'slave-01': ['controller']})

        self.show_step(12)
        self.fuel_web.deploy_cluster_wait(
            cluster_id,
            check_services=False
        )
        self.show_step(13)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            should_fail=0,
            test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(14)
        TestPluginCheck(self).plugin_check()
