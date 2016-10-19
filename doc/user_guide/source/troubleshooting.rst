Troubleshooting
---------------

This section contains a guidance on how to ensure that the Manila plugin is up
and running on your deployed environment.

**To find logs**

The Manila places its log by convinient path. On controller:

* ``/var/log/manila/manila-api.log``
* ``/var/log/manila/manila-scheduler.log``

On a manila-share node:

* ``/var/log/manila/manila-share.log``

On a manilsa-data node

* ``/var/log/manila/manila-data.log``

**To verify Manila configuragion files**

Check that ``/etc/manila`` directory contains following files:

* ``-rw-r--r-- 1 manila manila 1.8K Oct 19 02:35 api-paste.ini``
* ``-rw-r--r-- 1 manila manila 1.3K Oct 19 02:35 logging_sample.conf``
* ``-rw-r--r-- 1 root   root   2.6K Oct 19 03:44 manila.conf``
* ``-rw-r--r-- 1 manila manila 5.2K Oct 19 02:35 policy.json``
* ``-rw-r--r-- 1 root   root    989 Oct 19 02:35 rootwrap.conf``
* ``drwxr-xr-x 2 manila manila 4.0K Oct 19 02:35 rootwrap.d``

**To verify Manila services**

Check output of the commands on any controller node:

  .. code-block:: console

     # . /root/openrc
     # manila service-list

All services should be in the *up* stage.

**In case of using self signed certificates**

Use the ``--insecure`` option for all console commands. For example:

  .. code-block:: console

     # manila --insecure list
     # manila --insecure type-create some_share_type True
