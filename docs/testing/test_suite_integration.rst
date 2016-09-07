=================
Integration tests
=================


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


