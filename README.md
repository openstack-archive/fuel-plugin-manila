fuel-plugin-manila
==================

It is the plugin for Fuel that provide using Manila (File Share as a Service)
project whithin a Mirantis OpenStack's environment.

Installation
============

The Fuel Plugin Manila uses special service images from
https://github.com/openstack/manila-image-elements

Before installation that image should be placed on a Fuel master node and
environment variable MANILA_IMAGE should contain the path to that image.
