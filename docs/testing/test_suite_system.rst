============
System tests
============


NFS CIFS share with generic driver
----------------------------------


ID
##

manila_nfs_cifs_generic


Description
###########

Verify generic driver functionaity with CIFS and NFS share types

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 1 node with manila-share and 1 with manila-data role.
    4. Deploy cluster with plugin.
    5. Create configure and mount NFS share.
    6. Verify I/O to share according to configured ACL(IP).
    7. Create configure and mount CIFS share. 
    8. Verify I/O to share according to configured ACL(IP).


Expected results
################

All steps must be completed successfully, without any errors.


NFS CIFS share with generic driver
----------------------------------


ID
##

manila_nfs_cifs_netapp


Description
###########

Verify netapp driver functionaity with CIFS and NFS share types

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create an environment.
    3. Add at least 1 node with manila-share and 1 with manila-data role.
    4. Deploy cluster with plugin.
    5. Create configure and mount NFS share. 
    6. Verify I/O to NFS share according to configured ACL(IP).
    7. Create configure and mount CIFS share.
    8. Run instance with Windows based OS 
    9. Verify I/O to CIFS share according to configured ACL(LDAP).


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

Verify manila functionaity with CIFS and NFS share types and both drivers

Complexity
##########

core


Steps
#####


    1. Upload plugins and install.
    2. Create environment with both Generic and NetApp drivers enabled.
    3. Add at least 1 node with manila-share and 1 with manila-data role.
    4. Deploy cluster with plugin.
    5. Create configure and mount NFS share using generic driver. 
    6. Verify I/O to NFS share according to configured ACL(IP).
    7. Create configure and mount CIFS using NetApp driver.
    8. Run instance with Windows based OS 
    9. Verify I/O to CIFS share according to configured ACL(LDAP).


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