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
    3. Add a node with Controller role.
    4. Add a node with Compute + Cinder + Manila-share + Manila-data roles.
    5. Add a node with Base-OS role.
    6. Enable plugin for new environment
    7. Run network check
    8. Deploy cluster with plugin.

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

BVT test for manila plugin. Deploy cluster with a controller, a compute and
cinder roles and install Manila plugin.


Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create environment with "Neutron with VLAN segmentation" as 
       network configuration.
    3. Add 3 nodes with Controller role.
    4. Add 1 node with Cinder + Manila-share + Manila-data roles.
    5. Add 1 node with compute role.
    6. Enable plugin for new environment
    7. Deploy cluster with plugin.
    8. Run OSTF

Expected results
################

All steps must be completed successfully, without any errors.