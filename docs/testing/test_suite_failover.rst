Failover
========


Check cluster and manila functionality after controller shutdown/reboot
-----------------------------------------------------------------------

ID
##

manila_shut_reb_controller


Description
###########

Verify that manila-service works after controllers shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new ha environment.
    3. Add at least 3 nodes controller, 1 with manila-data and 1 with
       manila-share and 1 compute node roles.
    4. Deploy cluster.
    5. Shutdown primary controller node.
    6. Run OSTF.
    7. Verify Manila service basic functionality (share add/mount).
    8. Reboot controller node which becomes primary.
    9. Run OSTF.
    10. Verify Manila service basic functionality (share add/mount).


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after compute shutdown/reboot
--------------------------------------------------------------------

ID
##

manila_shut_reb_compute


Description
###########

Verify that manila-service works after compute shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new environment.
    3. Add at least 2 nodes compute role, 1 with manila-data and 1 with
       manila-share roles.
    4. Deploy cluster.
    5. Reboot first and shutdown second compute node.
    6. Run OSTF.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up compute second node, and shutdown first compute node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after manila-share shutdown/reboot
-------------------------------------------------------------------------

ID
##

manila_shut_reb_share


Description
###########

Verify that manila-service works after manila-share shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new environment.
    3. Add at least 2 nodes manila-share role, 1 with manila-data role.
    4. Deploy cluster.
    5. Shutdown first manila-share and reboot second manila-share node.
    6. Run OSTF.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up first manila-share node, and shutdown second manila-share node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after manila-data shutdown/reboot
-------------------------------------------------------------------------

ID
##

manila_shut_reb_data


Description
###########

Verify that manila-service works after manila-data shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new environment.
    3. Add at least 2 nodes manila-data role, 1 with manila-share role.
    4. Deploy cluster.
    5. Shutdown first manila-data and reboot second manila-data node.
    6. Run OSTF.
    7. Verify Manila service basic functionality (share add/mount).
    8. Bring up first manila-data node, and shutdown second manila-data node.
    9. Verify Manila service basic functionality (share add/mount).
    10. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.



Check cluster and manila functionality after cinder shutdown/reboot
-------------------------------------------------------------------

ID
##

manila_shut_reb_cinder


Description
###########

Verify that manila-service works after cinder shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new environment.
    3. Add at least 2 nodes cinder roles, 1 with manila-share and 1 with
       manila-share role.
    4. Deploy cluster.
    5. Run OSTF.
    6. Shutdown first and reboot second cinder node.
    7. Verify Manila service basic functionality (share add/mount).
    8. Run OSTF.
    9. Bring up first cinder node, and shutdown second cinder node.
    10. Verify Manila service basic functionality (share add/mount).
    11. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.


Check cluster and manila functionality after ceph-osd reboot
------------------------------------------------------------

ID
##

manila_shut_reb_ceph-osd


Description
###########

Verify that manila-service works after ceph-osd shutdown/reboot.


Complexity
##########

core


Steps
#####

    1. Install Manila plugin on master node.
    2. Create a new environment.
    3. Add at least 3 nodes ceph-osd roles, 1 with manila-share and 1 with
       manila-share role.
    4. Deploy cluster.
    5. Shutdown first ceph-osd node.
    6. Verify Manila service basic functionality (share add/mount).
    7. Run OSTF.
    8. Bring up first ceph-osd node and reboot second
    9. Verify Manila service basic functionality (share add/mount).
    10. Run OSTF.


Expected result
###############

All steps must be completed successfully, without any errors.