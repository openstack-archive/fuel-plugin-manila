================
Functional tests
================


Controller delete/add test
--------------------------


ID
##

manila_del_add_controllers


Description
###########

Verify that node with controller role can be deleted and added after deploying.

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 3 nodes with controller role.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).
    7. Delete a Controller node and deploy changes.
    8. Deploy cluster with plugin.
    9. Run OSTF.
    10. Verify Manila service basic functionality (share create/mount).
    11. Add a Controller node and deploy changes.
    12. Deploy cluster with plugin.
    13. Run OSTF.
    14. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Compute delete/add test
-----------------------


ID
##

manila_del_add_compute


Description
###########

Verify that node with compute role can be deleted and added after deploying.

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 2 nodes with compute role.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).
    7. Delete a compute node and deploy changes.
    8. Deploy cluster with plugin.
    9. Run OSTF.
    10. Verify Manila service basic functionality (share create/mount).
    11. Add a compute node and deploy changes.
    12. Deploy cluster with plugin.
    13. Run OSTF.
    14. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Cinder delete/add test
----------------------


ID
##

manila_del_add_cinder


Description
###########

Verify that node with cinder role can be deleted and added after deploying.

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 2 nodes with cinder role.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).
    7. Delete a cinder node and deploy changes.
    8. Deploy cluster with plugin.
    9. Run OSTF.
    10. Verify Manila service basic functionality (share create/mount).
    11. Add a cinder node and deploy changes.
    12. Deploy cluster with plugin.
    13. Run OSTF.
    14. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Manila-share delete/add test
----------------------------


ID
##

manila_del_add_share


Description
###########

Verify that node with manila-share role can be deleted and added after deploying.

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 2 nodes with manila-share role.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).
    7. Delete a manila-share node and deploy changes.
    8. Deploy cluster with plugin.
    9. Run OSTF.
    10. Verify Manila service basic functionality (share create/mount).
    11. Add a manila-share node and deploy changes.
    12. Deploy cluster with plugin.
    13. Run OSTF.
    14. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Manila-data delete/add test
---------------------------

ID
##

manila_del_add_data


Description
###########

Verify that node with manila-data role can be deleted and added after deploying.

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 2 nodes with manila-data role.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).
    7. Delete a manila-data node and deploy changes.
    8. Deploy cluster with plugin.
    9. Run OSTF.
    10. Verify Manila service basic functionality (share create/mount).
    11. Add a manila-data node and deploy changes.
    12. Deploy cluster with plugin.
    13. Run OSTF.
    14. Verify Manila service basic functionality (share create/mount).

Expected results
################

All steps must be completed successfully, without any errors.


Ceph add test
-------------


ID
##

manila_add_ceph


Description
###########

Verify that node with ceph-osd role can added after deploying.

Complexity
##########

core


Steps
#####

    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 3 nodes with ceph-osd role.
    4. Deploy cluster with plugin.
    5. Run OSTF.
    6. Verify Manila service basic functionality (share create/mount).
    7. Add another ceph-osd node and deploy changes.
    8. Deploy cluster with plugin.
    9. Run OSTF.
    10. Verify Manila service basic functionality (share create/mount).


Expected results
################

All steps must be completed successfully, without any errors.