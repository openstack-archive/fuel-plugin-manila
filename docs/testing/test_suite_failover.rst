Failover
========


Check cluster and manila functionality after controller shutdown/reboot
-----------------------------------------------------------------------

ID
##

manila_shutdown_controller


Description
###########

Verify that manila-service works after shutdown/reboot of controller.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new  ha environment.
    3. Add at least 3 nodes controller, 1 with manila-data and 1 with
       manila-share roles.
    4. Deploy cluster.
    5. Run OSTF.
    6. Shutdown primary controller node.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up controller node, and reboot second controller node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after compute shutdown
-------------------------------------------------------------

ID
##

manila_reboot_compute


Description
###########

Verify that manila-service works after compute shutdown.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new  environment.
    3. Add at least 2 nodes compute role, 1 with manila-data and 1 with
       manila-share roles.
    4. Deploy cluster.
    5. Run OSTF.
    6. Shutdown first compute node.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up compute node, and shutdown second compute node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Bring up second compute node.
    11. Verify Manila service basic functionality (share add/mount).
    12. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after manila-share shutdown/reboot
-------------------------------------------------------------------------

ID
##

manila_off_reboot_manila-share


Description
###########

Verify that manila-service works after manila-share shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new  environment.
    3. Add at least 2 nodes manila-share role, 1 with manila-data role.
    4. Deploy cluster.
    5. Run OSTF.
    6. Shutdown first manila-share and reboot second manila-share node.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up first manila-share node, and shutdown second manila-share node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Bring up second manila-share compute node.
    11. Verify Manila service basic functionality (share add/mount).
    12. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after manila-data shutdown/reboot
-------------------------------------------------------------------------

ID
##

manila_off_reboot_manila-data


Description
###########

Verify that manila-service works after manila-data shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new  environment.
    3. Add at least 2 nodes manila-data role, 1 with manila-share role.
    4. Deploy cluster.
    5. Run OSTF.
    6. Shutdown first manila-data and reboot second manila-data node.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up first manila-data node, and shutdown second manila-data node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Bring up second manila-share compute node.
    11. Verify Manila service basic functionality (share add/mount).
    12. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.



Check cluster and manila functionality after cinder shutdown
------------------------------------------------------------

ID
##

manila_off_reboot_cinder


Description
###########

Verify that manila-service works after cinder shutdown.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new  environment.
    3. Add at least 2 nodes cinder roles, 1 with manila-share and 1 with
       manila-share role.
    4. Deploy cluster.
    5. Run OSTF.
    6. Shutdown first cinder node.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up first cinder node, and shutdown second cinder node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Bring up second cinder node.
    11. Verify Manila service basic functionality (share add/mount).
    12. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after ceph-osd shutdown/reboot
---------------------------------------------------------------------

ID
##

manila_off_reboot_ceph-osd


Description
###########

Verify that manila-service works after ceph-osd shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new  environment.
    3. Add at least 3 nodes ceph-osd roles, 1 with manila-share and 1 with
       manila-share role.
    4. Deploy cluster.
    5. Run OSTF.
    6. Shutdown first ceph-osd node.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up first ceph-osd node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Reboot second ceph-osd node.
    11. Verify Manila service basic functionality (share add/mount).
    12. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.