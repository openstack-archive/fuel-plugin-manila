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
    """Integration test suite.

    The goal of integration testing is to ensure that Fuel Manila plugin work
    on cluster with different sets of roles, nodes, storage backends types
    will be used by QA to accept software builds from Development team.

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
            8. Reboot controller node which becomes primary.
            9. Run OSTF.
            10. Verify Manila service basic functionality (share add/mount).
        """

        self.env.revert_snapshot("ready_with_5_slaves")
        self.show_step(1)
        # plugin.install_manila_plugin(self.ssh_manager.admin_ip)
        # plugin.upload_manila_image(self.ssh_manager.admin_ip)

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={}
        )

        self.show_step(3)
        # plugin.enable_plugin_manila(cluster_id, self.fuel_web)
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller'],
             'slave-02': ['controller'],
             'slave-03': ['controller'],
             'slave-04': ['compute'],
             'slave-05': ['cinder']
             # 'slave-04': ['compute', 'manila-share'],
             # 'slave-05': ['cinder', 'manila-data']
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
        self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke',
                                                                 'sanity'])

        self.show_step(7)
        # TestPluginCheck(self).verify_manila_functionality()

        self.show_step(8)
        d_contr_2 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-02'))
        self.fuel_web.cold_restart_nodes([d_contr_2])

        self.show_step(9)
        self.fuel_web.run_ostf(cluster_id=cluster_id,
                               test_sets=['smoke', 'sanity'])

        self.show_step(10)
        # TestPluginCheck(self).verify_manila_functionality()

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["manila_shut_reb_compute"])
    @log_snapshot_after_test
    def manila_shut_reb_compute(self):
        """Check that manila-service works after compute shutdown/reboot.

        Scenario:
            1. Upload plugins and install.
            2. Create environment :
                * Networking: Neutron with VLAN segmentation
                * Block Storage: LVM
                * Other Storages: default
                * Additional services: disabled
            3. Enable plugin and add nodes with following roles:
                * Controller + Cinder + Manila-share + Manila-data
                * Compute
                * Compute
            4. Deploy cluster with plugin.
            5. Shutdown first and reboot second compute node.
            6. Run OSTF
            7. Verify Manila service basic functionality (share create/mount).
            8. Shutdown second and turn on first compute node
            9. Run OSTF.
            10. Verify Manila service basic functionality (share add/mount).
        """

        self.env.revert_snapshot("ready_with_3_slaves")
        self.show_step(1)
        # plugin.install_manila_plugin(self.ssh_manager.admin_ip)
        # plugin.upload_manila_image(self.ssh_manager.admin_ip)

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            settings={}
        )

        self.show_step(3)
        # plugin.enable_plugin_manila(cluster_id, self.fuel_web)
        self.fuel_web.update_nodes(
            cluster_id,
            {# 'slave-01': ['controller', 'cinder', 'manila-share',
             #              'manila-data'],
             'slave-01': ['controller', 'cinder'],
             'slave-02': ['compute'],
             'slave-03': ['compute']
             }
        )

        self.show_step(4)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        self.show_step(5)
        d_comp_1 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-02'))
        d_comp_2 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-03'))

        self.fuel_web.warm_shutdown_nodes([d_comp_1])
        self.fuel_web.cold_restart_nodes([d_comp_2], wait_online=True)

        self.show_step(6)
        cluster_id = self.fuel_web.get_last_created_cluster()
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity'],
            should_fail=1,
            failed_test_name=['Create volume and boot instance from it',
                              'Create volume and attach it to instance']
                               )

        self.show_step(7)
        # TestPluginCheck(self).verify_manila_functionality()

        self.show_step(8)
        self.fuel_web.warm_start_nodes([d_comp_1])
        self.fuel_web.warm_shutdown_nodes([d_comp_2])

        self.show_step(9)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id,
            test_sets=['smoke', 'sanity'],
            should_fail=1,
            failed_test_name=['Create volume and boot instance from it',
                              'Create volume and attach it to instance']
                               )

        self.show_step(10)
        # TestPluginCheck(self).verify_manila_functionality()

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["manila_shut_reb_cinder"])
    @log_snapshot_after_test
    def manila_shut_reb_cinder(self):
        """Check that manila-service works after cinder shutdown/reboot.

        Scenario:
            1. Upload plugins and install.
            2. Create environment :
                * Networking: Neutron with VLAN segmentation
                * Block Storage: LVM
                * Other Storages: default
                * Additional services: disabled
            3. Enable plugin and add nodes with following roles:
                * Controller + Manila-share + Manila-data
                * Compute
                * Cinder
                * Cinder
            4. Deploy cluster with plugin.
            5. Shutdown first and reboot second compute node.
            6. Run OSTF
            7. Verify Manila service basic functionality (share create/mount).
            8. Shutdown second and turn on first compute node
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
            {'slave-01': ['controller', 'manila-share', 'manila-data'],
             'slave-02': ['compute'],
             'slave-03': ['cinder'],
             'slave-04': ['cinder']
             }
        )

        self.show_step(4)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        self.show_step(5)
        d_cinder_1 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-03'))
        d_cinder_2 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-04'))

        self.fuel_web.warm_shutdown_nodes([d_cinder_1])
        self.fuel_web.cold_restart_nodes([d_cinder_2], wait_online=True)

        self.show_step(6)
        cluster_id = self.fuel_web.get_last_created_cluster()
        self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke',
                                                                 'sanity'])

        self.show_step(7)
        TestPluginCheck(self).verify_manila_functionality()

        self.show_step(8)
        self.fuel_web.warm_start_nodes([d_cinder_1])
        self.fuel_web.warm_shutdown_nodes([d_cinder_2])

        self.show_step(9)
        self.fuel_web.run_ostf(cluster_id=cluster_id,
                               test_sets=['smoke', 'sanity'])

        self.show_step(10)
        TestPluginCheck(self).verify_manila_functionality()

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["manila_shut_reb_ceph"])
    @log_snapshot_after_test
    def manila_shut_reb_ceph(self):
        """Check that manila-service works after ceph shutdown/reboot.

        Scenario:
            1. Upload plugins and install.
            2. Create environment :
                * Networking: Neutron with VLAN segmentation
                * Block Storage: LVM
                * Other Storages: default
                * Additional services: disabled
            3. Enable plugin and add nodes with following roles:
                * Controller + Ceph-OSD + Manila-share + Manila-data
                * Compute
                * Ceph-OSD
                * Ceph-OSD
                * Ceph-OSD
            4. Deploy cluster with plugin.
            5. Shutdown first and reboot second compute node.
            6. Run OSTF
            7. Verify Manila service basic functionality (share create/mount).
            8. Shutdown second and turn on first compute node
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
            settings={
                'volumes_ceph': True,
                'volumes_lvm': False,
                'ephemeral_ceph': True,
                'objects_ceph': True,
                'images_ceph': True
            }
        )

        self.show_step(3)
        plugin.enable_plugin_manila(cluster_id, self.fuel_web)
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller', 'ceph-osd', 'manila-share'],
             'slave-02': ['compute', 'manila-data'],
             'slave-03': ['ceph-osd'],
             'slave-04': ['ceph-osd'],
             'slave-05': ['ceph-osd'],
             }
        )

        self.show_step(4)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        self.show_step(5)
        d_ceph_1 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-03'))
        d_ceph_2 = self.fuel_web.get_devops_node_by_nailgun_node(
            self.fuel_web.get_nailgun_node_by_base_name(
                base_node_name='slave-04'))

        self.fuel_web.warm_shutdown_nodes([d_ceph_1])

        self.show_step(6)
        cluster_id = self.fuel_web.get_last_created_cluster()
        self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke',
                                                                 'sanity'])
        self.show_step(7)
        TestPluginCheck(self).verify_manila_functionality()

        self.show_step(8)
        self.fuel_web.warm_start_nodes([d_ceph_1])
        self.fuel_web.warm_shutdown_nodes([d_ceph_2])

        self.show_step(9)
        self.fuel_web.run_ostf(cluster_id=cluster_id,
                               test_sets=['smoke', 'sanity'])

        self.show_step(10)
        TestPluginCheck(self).verify_manila_functionality()
