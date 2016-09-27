============
System tests
============


NFS share with generic driver
-----------------------------


ID
##

manila_nfs_generic


Description
###########

Verify generic driver functionality with NFS share type.

Complexity
##########

cores


Steps
#####


    1. Upload plugins and install.
    2. Create an environment with manila plugin and configured generic driver.
    3. Add at least 1 manila-share 1 manila-data 1 compute nodes role.
    4. Deploy cluster with plugin.
    5. Create configure and mount NFS share.
    6. Verify I/O to share according to configured ACL(IP).

Expected results
################

All steps must be completed successfully, without any errors.


CIFS share with generic driver
------------------------------


ID
##

manila_cifs_generic


Description
###########

Verify generic driver functionality with CIFS share type.

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment with manila plugin and configured generic driver.
    3. Add at least 1 manila-share 1 manila-data 1 compute nodes role.
    4. Deploy cluster with plugin.
    5. Create configure and mount CIFS share.
    6. Verify I/O to share according to configured ACL(IP).


Expected results
################

All steps must be completed successfully, without any errors.


NFS share with netapp driver
----------------------------


ID
##

manila_nfs_netapp


Description
###########

Verify netapp driver functionality with NFS share type.

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment with manila plugin and configured netapp driver.
    3. Add at least 1 manila-share 1 manila-data 1 compute nodes role.
    4. Deploy cluster with plugin.
    5. Create configure and mount NFS share.
    6. Verify I/O to share according to configured ACL(IP).


Expected results
################

All steps must be completed successfully, without any errors.


ID
##

manila_cifs_netapp


Description
###########

Verify netapp driver functionality with CIFS and NFS share types

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment with manila plugin and configured netapp driver.
    3. Add at least 1 manila-share 1 manila-data 1 compute nodes role.
    4. Deploy cluster with plugin.
    5. Create configure and mount CIFS share.
    6. Verify I/O to NFS share according to configured ACL(IP).


Expected results
################

All steps must be completed successfully, without any errors.


NFS CIFS share with both drivers
--------------------------------


ID
##

manila_nfs_cifs_both


Description
###########

Verify manila functionaity with and both generic and netapp drivers enabled

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create environment with both Generic and NetApp drivers enabled.
    3. Add at least 1 manila-share 1 manila-data 1 compute nodes role.
    4. Deploy cluster with plugin.
    5. Create configure and mount NFS share using generic driver.
    6. Verify I/O to NFS share according to configured ACL(IP).
    7. Create configure and mount CIFS using NetApp driver.
    8. Verify I/O to NFS share according to configured ACL(IP).


Expected results
################

All steps must be completed successfully, without any errors.


Instance live migration
-----------------------


ID
##

manila_live_migration


Description
###########

Verify manila functionaity after instance live migration

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create environment with both Generic.
    3. Add at least 2 nodes with compute role 1 node with manila-share and
       1 with manila-data role
    4. Deploy cluster with plugin.
    5. Create configure and mount NFS share using generic driver.
    6. Verify I/O to NFS share.
    7. Execute live migration for instance to other compute.
    8. Verify I/O to NFS share after migration.


Expected results
################

All steps must be completed successfully, without any errors.