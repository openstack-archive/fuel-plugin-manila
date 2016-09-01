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

from proboscis import test

from fuelweb_test.helpers.decorators import log_snapshot_after_test
from fuelweb_test.tests.base_test_case import TestBasic
from fuelweb_test.tests.base_test_case import SetupEnvironment
from fuelweb_test.settings import DEPLOYMENT_MODE
from fuelweb_test.settings import NEUTRON_SEGMENT

from helpers import plugin
from helpers import settings
from helpers import manila_service_verify

# set_default
path = "/var/www/nailgun/plugins/fuel-plugin-manila-1.0/repositories" \
       "/ubuntu"


@test(groups=['manila_plugin', 'manila_integration'])
class TestManilaIntegration(TestBasic):
    """Integration test suite.

    The goal of integration testing is to ensure that Fuel Manila plugin work
    on cluster with different sets of roles, nodes, storage beckends typs
    will be used by QA to accept software builds from Development team.

    """

    @test(depends_on=[SetupEnvironment.prepare_slaves_5],
          groups=["manila_controller_ha"])
    @log_snapshot_after_test
    def manila_controller_ha(self):
        """Check cluster deploy in HA mode (3 controllers).Using Ceph as a back
         end for block storage.

        Scenario:
            1. Upload plugin and install.
            2. Create environment :
                * Compute: KVM/QEMU
                * Networking: Neutron with tunneling segmentation
                * Block Storage: Ceph
                * Other Storages: default
                * Additional services: disabled
            3. Enable plugin and add nodes with following roles:
                * Controller + Cinder
                * Controller + Ceph-OSD
                * Controller + Ceph-OSD
                * Compute
                * Ceph-OSD + Manila-Share + Manila-Data.
            4. Deploy cluster with plugin.
            5. Run OSTF.
            6. Verify Manila service basic functionality (share create/mount).
        """

        self.env.revert_snapshot("ready_with_5_slaves")
        self.show_step(1)
        plugin.install_manila_plugin(self.ssh_manager.admin_ip)
        # upload manila image to master node
        plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

        self.show_step(2)
        # Configure new cluster

        cluster_id = self.fuel_web.create_cluster(
            name=self.__class__.__name__,
            mode=DEPLOYMENT_MODE,
            settings={
                "net_provider": 'neutron',
                "net_segment_type": NEUTRON_SEGMENT['tun'],
                'volumes_ceph': True
            },
            configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
        )

        self.show_step(3)
        plugin.enable_plugin_manila(cluster_id, self.fuel_web)
        # Assign role to node
        self.fuel_web.update_nodes(
            cluster_id,
            {'slave-01': ['controller', 'cinder'],
             'slave-02': ['controller', 'ceph-osd'],
             'slave-03': ['controller', 'ceph-osd'],
             'slave-04': ['compute'],
             'slave-05': ['ceph-osd', 'manila-share', 'manila-data']
             }
        )

        self.show_step(4)
        self.fuel_web.deploy_cluster_wait(cluster_id)

        self.show_step(5)
        self.fuel_web.run_ostf(
            cluster_id=cluster_id, test_sets=['smoke', 'sanity', 'ha'])

        self.show_step(6)
        # verify manila services after deploy
        cluster_id = self.fuel_web.get_last_created_cluster()
        os_ip = self.fuel_web.get_public_vip(cluster_id)
        manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_two_computes"])
@log_snapshot_after_test
def manila_two_computes(self):
    """Check cluster deploy with Manila Plugin and two nodes with compute role.

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with VLAN segmentation
            * Block Storage: LVM
            * Other Storages: default
            * Additional services: disabled
        3. Enable plugin and add nodes with following roles:
            * Controller
            * Compute + Manila-share + Manila-Data roles
            * Compute + Cinder
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).
    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['vlan'],
            'volumes_ceph': False
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller'],
         'slave-02': ['compute', 'manila-share', 'manila-data'],
         'slave-03': ['compute', 'cinder']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(
        cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_two_cinders"])
@log_snapshot_after_test
def manila_two_cinders(self):
    """Check cluster deploy with Manila Plugin and two nodes with cinder role.

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with tunneling segmentation
            * Block Storage: LVM
            * Other Storages: default
            * Additional services: disabled
        3. Enable plugin and add nodes with following roles:
            * Controller + Manila-share + Manila-Data
            * Compute + Cinder
            * Cinder
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).
    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['tun'],
            'volumes_ceph': False
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller'],
         'slave-02': ['cinder', 'manila-share', 'manila-data'],
         'slave-03': ['compute', 'cinder']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(
        cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_share_ha"])
@log_snapshot_after_test
def manila_share_ha(self):
    """Check cluster deploy with Manila Plugin and two nodes with Manila-share
    role.

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with VLAN segmentation
            * Block Storage: LVM
            * Other Storages: default
            * Additional services: disabled
        3. Enable plugin and add nodes with following roles:
            * Controller + Manila-share
            * Compute + Manila-share
            * Cinder + Manila-data
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).
    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['vlan'],
            'volumes_ceph': False
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller', 'manila-share'],
         'slave-02': ['compute', 'manila-share'],
         'slave-03': ['cinder', 'manila-data']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_data_ha"])
@log_snapshot_after_test
def manila_share_ha(self):
    """Check cluster deploy with Manila Plugin and two nodes with Manila-data
    role.

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with tunneling segmentation
            * Block Storage: LVM
            * Other Storages: default
            * Additional services: disabled
        3. Enable plugin and add nodes with following roles:
            * Controller + Manila-data
            * Compute + Manila-data
            * Cinder + Manila-share
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).
    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['vlan'],
            'volumes_ceph': False
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller', 'manila-data'],
         'slave-02': ['compute', 'manila-data'],
         'slave-03': ['cinder', 'manila-share']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_both_cinder_ceph"])
@log_snapshot_after_test
def manila_both_cinder_ceph(self):
    """Deploy a cluster using Ceph as a backend for block storage and cinder for
     other (image, object and ephemeral).

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with tunneling segmentation
            * Block Storage: Ceph
            * Other Storages: default
            * Additional services: disabled
        3. Enable plugin and add nodes with following roles:
            * Controller + Cinder + Ceph-OSD
            * Compute + Ceph-OSD + Manila-data
            * Ceph-OSD + Manila-share
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).
    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['tun'],
            'volumes_ceph': True
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller', 'cinder', 'ceph-osd'],
         'slave-02': ['compute', 'ceph-osd', 'manila-data'],
         'slave-03': ['ceph-osd', 'manila-share']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_all_ceph"])
@log_snapshot_after_test
def manila_all_ceph(self):
    """Deploy a cluster using Ceph as a backend for block storage and cinder for
     other (image, object and ephemeral).

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with VLAN segmentation
            * Block Storage: Ceph
            * Other Storages: all Ceph
            * Additional services: disabled
        3. Enable plugin and add nodes with following roles:
            * Controller + Ceph-OSD + Manila-data
            * Compute + Ceph-OSD
            * Ceph-OSD + Manila-share
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).
    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['vlan'],
            'volumes_ceph': True,
            'volumes_lvm': False
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller', 'ceph-osd', 'manila-data'],
         'slave-02': ['compute', 'ceph-osd'],
         'slave-03': ['ceph-osd', 'manila-share']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_with_ceilometer"])
@log_snapshot_after_test
def manila_with_ceilometer(self):
    """Deploy a cluster with additional component Ceilometer

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with tunneling segmentation
            * Block Storage: Ceph
            * Other Storages: all Ceph
            * Additional services: Ceilometer
        3. Enable plugin and add nodes with following roles:
            * Controller + Ceph-OSD
            * Compute + Ceph-OSD + Manila-share
            * Ceph-OSD + Manila-data
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).

    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['tun'],
            'volumes_lvm': False,
            'volume-ceph': True,
            "image-ceph": True,
            "ephemeral-ceph": True,
            "objects_ceph": True,
            "ceilometer": True
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller', 'ceph-osd'],
         'slave-02': ['compute', 'ceph-osd', 'manila-share'],
         'slave-03': ['ceph-osd', 'manila-data']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_with_ceilometer"])
@log_snapshot_after_test
def manila_with_murano(self):
    """Deploy a cluster with additional component Murano

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with vlan segmentation
            * Block Storage: Ceph
            * Other Storages: all Ceph
            * Additional services: Murano
        3. Enable plugin and add nodes with following roles:
            * Controller + Ceph-OSD
            * Compute + Ceph-OSD + Manila-share
            * Ceph-OSD + Manila-data
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).

    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['vlan'],
            'volumes_lvm': False,
            'volume-ceph': True
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller', 'ceph-osd', 'manila-data'],
         'slave-02': ['compute', 'ceph-osd', 'cinder'],
         'slave-03': ['ceph-osd', 'manila-share']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)


@test(depends_on=[SetupEnvironment.prepare_slaves_3],
      groups=["manila_with_sahara"])
@log_snapshot_after_test
def manila_with_murano(self):
    """Deploy a cluster with additional component Sahara

    Scenario:
        1. Upload plugins and install.
        2. Create environment :
            * Compute: KVM/QEMU
            * Networking: Neutron with tunneling segmentation
            * Block Storage: LVM (Cinder)
            * Other Storages: Ceph
            * Additional services: Sahara
        3. Enable plugin and add nodes with following roles:
            * Controller + Manila-share + Ceph-OSD
            * Compute + Ceph-OSD + Manila-data
            * Ceph-OSD + Cinder
        4. Deploy cluster with plugin.
        5. Run OSTF
        6. Verify Manila service basic functionality (share create/mount).

    """

    self.env.revert_snapshot("ready_with_3_slaves")
    self.show_step(1)
    plugin.install_manila_plugin(self.ssh_manager.admin_ip)
    # upload manila image to master node
    plugin.upload_manila_image(self.ssh_manager.admin_ip, path)

    self.show_step(2)
    # Configure new cluster

    cluster_id = self.fuel_web.create_cluster(
        name=self.__class__.__name__,
        mode=DEPLOYMENT_MODE,
        settings={
            "net_provider": 'neutron',
            "net_segment_type": NEUTRON_SEGMENT['tun'],
            "image-ceph": True,
            "objects_ceph": True,
            "ephemeral-ceph": True
        },
        configure_ssl=settings.CLUSTER_ENDPOINT_USE_SSL
    )

    self.show_step(3)
    plugin.enable_plugin_manila(cluster_id, self.fuel_web)
    # Assign role to node
    self.fuel_web.update_nodes(
        cluster_id,
        {'slave-01': ['controller', 'manila-share', 'ceph-osd'],
         'slave-02': ['compute', 'ceph-osd', 'manila-data'],
         'slave-03': ['ceph-osd', 'cinder']
         }
    )

    self.show_step(4)
    self.fuel_web.deploy_cluster_wait(cluster_id)

    self.show_step(5)
    self.fuel_web.run_ostf(cluster_id=cluster_id, test_sets=['smoke', 'sanity'])

    self.show_step(6)
    # verify manila services after deploy
    cluster_id = self.fuel_web.get_last_created_cluster()
    os_ip = self.fuel_web.get_public_vip(cluster_id)
    manila_service_verify.basic_functionality(os_ip)
