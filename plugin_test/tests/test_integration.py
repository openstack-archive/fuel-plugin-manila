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


from helpers.manila_service_verify import TestPluginCheck
from helpers import plugin
from proboscis import test


@test(groups=['manila_plugin', 'manila_integration'])
class TestManilaIntegration(TestBasic):
    """Integration test suite.

    The goal of integration testing is to ensure that Fuel Manila plugin work
    on cluster with different sets of roles, nodes, storage beckends typs
    will be used by QA to accept software builds from Development team.

    """

    @test(depends_on=[SetupEnvironment.prepare_slaves_3],
          groups=["manila_share_ha"])
    @log_snapshot_after_test
    def manila_share_ha(self):
        """Check cluster deploy with Manila Plugin and two Manila-share roles.

        Scenario:
            1. Upload plugins and install.
            2. Create environment :
                * Compute: KVM/QEMU
                * Networking: Neutron with VLAN segmentation
                * Block Storage: Ceph
                * Other Storages: default
                * Additional services: disabled
            3. Enable plugin and add nodes with following roles:
                * Controller + Manila-share + Ceph-OSD
                * Compute + Manila-share + Ceph-OSD
                * Cinder + Manila-data + Ceph-OSD
            4. Deploy cluster with plugin.
            5. Run OSTF
            6. Verify Manila service basic functionality (share create/mount).
        """

        self.env.revert_snapshot("ready_with_3_slaves")
        self.show_step(1)
        plugin.install_manila_plugin(self.ssh_manager.admin_ip)
        plugin.upload_manila_image(self.ssh_manager.admin_ip)

        self.show_step(2)
        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT,
                'volumes_ceph': True,
                'volumes_lvm': False
            },
        )

        self.show_step(3)
        plugin.enable_plugin_manila(cluster_id, self.fuel_web)
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller', 'manila-share', 'ceph-osd'],
             'slave-02': ['compute', 'manila-share', 'ceph-osd'],
             'slave-03': ['cinder', 'manila-data', 'ceph-osd']
             }
        )

        self.show_step(4)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        self.show_step(5)
        self.fuel_web.run_ostf(cluster_id=cluster_id,
                               test_sets=['smoke', 'sanity'])

        self.show_step(6)
        # verify manila services after deploy
        TestPluginCheck(self).verify_manila_functionality()


