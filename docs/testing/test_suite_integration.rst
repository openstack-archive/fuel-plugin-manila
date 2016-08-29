=================
Integration tests
=================


Controller HA test
------------------


ID
##

manila_controller_HA


Description
###########

Check cluster deploy in HA mode (3 controllers).Using Ceph as a back end for
block storage.


Complexity
##########

core


Steps
#####

    1. Upload plugin and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with tunneling segmentation
        * Block Storage: Ceph
        * Other Storages: default
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Cinder
        * Controller + Ceph-OSD
        * Controller + Ceph-OSD
        * Compute
        * Ceph-OSD + Manila-Share + Manila-Data.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Multiple computes test
----------------------


ID
##

manila_two_computes


Description
###########

Deploy a cluster with Manila Plugin and two nodes with compute role.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with VLAN segmentation
        * Block Storage: LVM
        * Other Storages: default
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller
        * Compute + Manila-share + Manila-Data roles
        * Compute + Cinder
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Multiple cinder nodes test
--------------------------


ID
##

manila_two_cinders


Description
###########

Deploy a cluster with Manila Plugin and two nodes with cinder role.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with tunneling segmentation
        * Block Storage: LVM
        * Other Storages: default
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Manila-share + Manila-Data
        * Compute + Cinder
        * Cinder
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Multiple manila share nodes test
--------------------------------


ID
##

manila_share_HA


Description
###########

Deploy a cluster with two nodes with Manila-share role.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with VLAN segmentation
        * Block Storage: LVM
        * Other Storages: default
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Manila-share
        * Compute + Manila-share
        * Cinder + Manila-data
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Multiple manila share nodes test
--------------------------------


ID
##

manila_data_HA


Description
###########

Deploy a cluster with two nodes with Manila-data role.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with tunneling segmentation
        * Block Storage: LVM
        * Other Storages: default
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Manila-data
        * Compute + Manila-data
        * Cinder + Manila-share
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


ID
##

manila_both_cinder_ceph


Description
###########

Deploy a cluster using Ceph as a backend for block storage and cinder for other (image, object and ephemeral).

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with tunneling segmentation
        * Block Storage: Ceph
        * Other Storages: default
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Cinder + Ceph-OSD
        * Compute + Ceph-OSD + Manila-data
        * Ceph-OSD + Manila-share
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.

ID
##

manila_all_ceph


Description
###########

Deploy a cluster with using Ceph as a backend for all storages.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with VLAN segmentation
        * Block Storage: Ceph
        * Other Storages: all Ceph
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Ceph-OSD + Manila-data
        * Compute + Ceph-OSD
        * Ceph-OSD + Manila-share
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.

ID
##

manila_with_ceilometer


Description
###########

Deploy a cluster with using Ceph as a backend for all storages.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with tunneling segmentation
        * Block Storage: Ceph
        * Other Storages: all Ceph
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Ceph-OSD
        * Compute + Ceph-OSD + Manila-share
        * Ceph-OSD + Manila-data
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


ID
##

manila_with_murano


Description
###########

Deploy a cluster with using Ceph as a backend for all storages.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with VLAN segmentation
        * Block Storage: Ceph
        * Other Storages: default (Cinder)
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Ceph-OSD + Manila-data
        * Compute + Ceph-OSD + Cinder
        * Ceph-OSD + Manila-share
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


ID
##

manila_with_sahara


Description
###########

Deploy a cluster with additional component Sahara

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment :
        * Compute: KVM/QEMU
        * Networking: Neutron with tunneling segmentation
        * Block Storage: LVM (Cinder)
        * Other Storages: Ceph
        * Additional services: disabled
    3. Add nodes with following roles:
        * Controller + Manila-share + Ceph-OSD
        * Compute + Ceph-OSD + Manila-data
        * Ceph-OSD + Cinder
    4. Deploy cluster with plugin.
    5. Run OSTF
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.