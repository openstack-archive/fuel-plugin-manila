..
 This work is licensed under a Creative Commons Attribution 3.0 Unported
 License.

 http://creativecommons.org/licenses/by/3.0/legalcode

==========================================
Fuel Manila plugin
==========================================

https://blueprints.launchpad.net/fuel-plugin-manila/+spec/initial-9.0

There is the Fuel plugin that installs and configures the Manila [0]_.

--------------------
Problem description
--------------------

There is the Manila project that provides a shared file system service for
OpenStack. It's the new OpenStack project that provides coordinated access
to shared or distributed file systems. The Manila has multiple storage
backends (to support vendor or file system specific nuances/capabilities) that
could work simultaneously on one environment.

The Fuel Manila plugin adds utilization the corresponding OpenStack service
in an Fuel environment.

----------------
Proposed changes
----------------

Install the Manila and Python Manila Client. Upload the service image into
glance if enabled drivers requires it. Create shared network for providing
access to a network shares.

::-
                                   |  Management  | Public
                                   |  Private     |
                                   |  Storage     |
                                   |              |
    +---------------------+        |              |    +------------+
    |Controller           |        |              |    |An external |
    |+------------------+ |        |              +----+Storage     |
    ||Pacemaker         | |        |              |    +------------+
    || manila-api       | +--------+              |
    || manila-scheduler | |        |              |
    || manila-share     | |        |              |
    || manila-data      | +--------o--------------+
    |+------------------+ |        |              |
    | glance-api          |        |              |
    | cinder-api          |        |              |
    +---------------------+        |              |
                                   |              |
    +---------------------+        |              |
    |Cinder               |        |              |
    | cinder-volume       +--------+              |
    +---------------------+        |              |
                                   |              |
    +---------------------+        |              |
    |Compute              |        |              |
    | nova-compute        +--------+              |
    +---------------------+        |              |
                                   |              |

Web UI
======

A user will have possibilities to chose a storage backends and its parameters.


Nailgun
=======

None

Data model
----------

New database, tables and account to database access.

REST API
--------

None

Orchestration
=============

None


RPC Protocol
------------

None

Fuel Client
===========

None

Plugins
=======

The Fuel Manila plugin doesn't interact with others.


Fuel Library
============

None

------------
Alternatives
------------

Deploy an environment with Cinder and Compute nodes, install and configure
the Manila manually.

--------------
Upgrade impact
--------------

None

---------------
Security impact
---------------

None

--------------------
Notifications impact
--------------------

None

---------------
End user impact
---------------

Manila has CLI [1]_ and Web [2]_ UI. Both of  them will be deployed by the plugin.

------------------
Performance impact
------------------

None

-----------------
Deployment impact
-----------------

For generic driver service image [3]_ will be required on each deployment.

----------------
Developer impact
----------------

None


---------------------
Infrastructure impact
---------------------

None

--------------------
Documentation impact
--------------------

* Deployment Guide (how to prepare an environment for installation, how to
  install the plugin, how to deploy OpenStack an environment with the plugin).

* User Guide (which features the plugin provides, how to use them in the
  deployed OS environment).

* Test Plan.

* Test Report.


--------------
Implementation
--------------

Assignee(s)
===========
Primary assignee:
  Igor Gajsin <igajsin>

QA:
  Oleksandr Kosse <okosse>,
  Yevgeniy Shapovalov <yshapovalov>

Mandatory design review:
  Igor Gajsin <igajsin>


Work Items
==========

* Build infrastructure for the project.

* Install certain packages and programs.

* Do keystone stuff (users, endpoints end so on).

* Create DB user, database and populate it.

* Configure the manila with generic driver.

* Add haproxy and iptables rules.

* Add init scripts.

* Install service image, create storage network

* Add Horizon parts.

* Configure the manila with netapp driver.

* (optional) Add OSTF tests for Manila


Dependencies
============

The Fuel Manila plugin depends on the whole Manila project. See links in the
section "References".

------------
Testing, QA
------------

Will be improved by QA.


Acceptance criteria
===================

Will be improved by QA.

----------
References
----------

* https://wiki.openstack.org/wiki/Manila

* https://github.com/openstack/python-manilaclient

* https://github.com/openstack/manila-ui

* https://github.com/openstack/manila-image-elements
