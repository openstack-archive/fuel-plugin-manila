=================
Integration tests
=================


Controller HA test
------------------


ID
##

manila_controller_ha


Description
###########

Check cluster deploy in HA mode (3 controllers).


Complexity
##########

core


Steps
#####
    1. Upload plugins and install.
    2. Create environment with at least 3 Controller, 1 Compute, 1 Cinder,
       1 Manila-share and 1 Manila-data roles.
    3. Deploy cluster with plugin.
    4. Run OSTF.
    5. Verify Manila service basic functionality (share create/mount).

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

Deploy a cluster with  at least two Compute nodes.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with at least 2 Computes, 1 controller, 1 Cinder,
       1 Manila-share and 1 Manila-data roles.
    3. Deploy cluster with plugin.
    4. Run OSTF.
    5. Verify Manila service basic functionality (share create/mount).

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

Deploy a cluster with Manila Plugin and at least two nodes with cinder role.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with at least 2 Computes, 1 controller, 1 Cinder,
       1 Manila-share and 1 Manila-data roles.
    3. Deploy cluster with plugin.
    4. Run OSTF.
    5. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Multiple manila share nodes test
--------------------------------


ID
##

manila_share_ha


Description
###########

Deploy a cluster with at least two nodes with Manila-share role.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with at least 2 Manila-share , 1 controller,
       1 Cinder, 1 Compute and 1 Manila-data roles.
    3. Deploy cluster with plugin.
    4. Run OSTF.
    5. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Multiple manila data nodes test
--------------------------------


ID
##

manila_data_ha


Description
###########

Deploy a cluster with two nodes with Manila-data role.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with at least 2 Manila-data , 1 controller,
       1 Cinder, 1 Compute and 1 Manila-share roles.
    3. Deploy cluster with plugin.
    4. Run OSTF.
    5. Verify Manila service basic functionality (share create/mount)

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
    2. Set Ceph as a backend for block storage
    3. Create environment with at least 1 Manila-data, 1 controller,
       1 Cinder, 1 Compute 1 Manila-share and 3 Ceph-OSD roles.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount)

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
    2. Set Ceph as a backend for all type of storages
    3. Create environment with at least 1 Manila-data, 1 controller, 1 Compute
       1 Manila-share and 3 Ceph-OSD roles.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.

ID
##

manila_with_ceilometer


Description
###########

Deploy a cluster with additional component Ceilometer.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with enabled component Ceilometer.
    3. Configure nodes: at least 1 Manila-data, 1 controller, 1 Compute 
       1 Manila-share and 3 Ceph-OSD roles.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


ID
##

manila_with_murano


Description
###########

Deploy a cluster with additional component Murano.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with enabled component Murano.
    3. Configure nodes: at least 1 Manila-data, 1 controller, 1 Compute
       1 Manila-share and 3 Ceph-OSD roles.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


ID
##

manila_with_sahara


Description
###########

Deploy a cluster with additional component Sahara.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with enabled component Sahara.
    3. Configure nodes: at least 1 Manila-data, 1 controller, 1 Compute
       1 Manila-share and 3 Ceph-OSD roles.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.