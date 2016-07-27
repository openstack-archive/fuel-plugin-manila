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
    2. Create environment with "Neutron with tunneling segmentation" as 
       a network configuration.
    3. Add a node with controller role.
    4. Add a node with compute role.
    5. Add a node with cinder role.
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
    2. Create environment with "Neutron with tunneling segmentation" as network configuration.
    3. Add 3 nodes with controller and cinder roles.
    4. Add 2 node with compute roles.
    5. Enable plugin for new environment
    6. Deploy cluster with plugin.
    7. Run OSTF

Expected results
################

All steps must be completed successfully, without any errors.