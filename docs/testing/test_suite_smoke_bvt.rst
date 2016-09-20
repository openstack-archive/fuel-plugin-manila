===============
Smoke/BVT tests
===============


Instalation test
----------------


ID
##

manila_install


Description
###########

Check install/uninstall Manila Plugin functionality.


Complexity
##########

core


Steps
#####

    1. Upload plugins to the master node and install.
    2. Create a new environment
    3. Enable Manila plugin for new environment.
    4. Attempt to remove enabled plugin.
    5. Disable  plugin
    6. Remove Plugin Manila

Expected results
################

All steps must be completed successfully, without any errors.


Smoke test
----------


ID
##

manila_smoke


Description
###########

Deploy a cluster with Manila Plugin.


Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with "Neutron with VLAN segmentation" as
       a network configuration.
    3. Enable plugin.
    4. Configure environment:
        * Add a node with Controller + role.
        * Add a node with Compute + Cinder + Manila-share + Manila-data roles.
        * Add a node with Compute + Cinder roles.
    5. Run network check
    6. Deploy cluster with plugin.
    7. Verify Manila service basic functionality (share add/mount)

Expected results
################

All steps must be completed successfully, without any errors.


BVT test
----------


ID
##

manila_bvt


Description
###########

BVT test for manila plugin. Deploy cluster with 3 controller and install Manila plugin.


Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with "Neutron with tunneling segmentation" as
       a network configuration.
    3. Enable plugin.
    4. Configure environment:
        * Add a node with Controller + Ceph-OSD roles.
        * Add a node with Controller + Ceph-OSD roles.
        * Add a node with Controller + Ceph-OSD roles.
        * Add a node with Compute + Ceph-OSD roles.
        * Add a node with Ceph-osd + Manila-share + Manila-data roles.
    5. Deploy cluster with plugin.
    6. Run OSTF.
    7. Verify Manila service basic functionality (share add/mount)

Expected results
################

All steps must be completed successfully, without any errors.