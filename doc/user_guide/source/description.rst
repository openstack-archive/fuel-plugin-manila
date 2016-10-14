.. _overview:

Overview of the Manila plugin for Fuel
--------------------------------------

The purpose of this document is to describe how to install, configure and use
the Manila plugin 1.0.0 for Fuel 9.1

The Manila is the OpenStack project that provides "File Sharing as a Service".
Main goal of the project is providing coordinated access to shared or
distributed file systems to OpenStack Compute instances. But as a many other
OpenStack services it can be used independently according to modular design
established by OpenStack.

The Manila based on that principes:

* Component based architecture: Quickly add new behaviors

* Highly available: Scale to very serious workloads

* Fault-Tolerant: Isolated processes avoid cascading failures

* Recoverable: Failures should be easy to diagnose, debug, and rectify

* Open Standards: Be a reference implementation for a community-driven api

* API Compatibility: Manila strives to provide API-compatible with popular
  systems like Amazon EC2

This plugin brings features of Manila into Mirantis OpenStack.


.. _pg-requirements:

Software prerequisites
----------------------

To use the Manila plugin for Fuel 9.1, verify that your environment meets
the following prerequisites:

======================= =================================
Prerequisites           Version/Comment
======================= =================================
Fuel                    9.1
manila-service-image    last
NetApp® ONTAP®          8 or later
======================= =================================

The manila-service image is the service image for generic driver. It should be
build from https://github.com/openstack/manila-image-elements.

   .. raw:: latex

      \pagebreak


Limitations
-----------

The Manila plugin for Fuel 9.1 has some known issues/limitations of usage:

* Manila CLI response with warnings if specific configuration
  https://bugs.launchpad.net/fuel-plugin-manila/+bug/1633018

* Manila services uses publicURL instead of internalURL
  https://bugs.launchpad.net/fuel-plugin-manila/+bug/1633456
