
.. _pg-install:

Install Manila plugin for Fuel
------------------------------

Before you install Manila plugin for Fuel 9.1, verify that your environment
meets the requirements described in :ref:`pg-requirements`. You must have
the Fuel Master node installed and configured before you can install
the plugin. This plugin is hotpluggable, so you can install the Manila plugin
for Fuel after you deploy an OpenStack environment.

**To install Manila plugin for Fuel:**

#. Download Manila plugin for Fuel from the `Fuel Plugins Catalog`_.

#. Copy the plugin ``.rpm`` package to the Fuel Master node:

   **Example:**

   .. code-block:: console

      # scp fuel-plugin-manila-1.0-1.0.0-1.noarch.rpm root@fuel-master:/tmp

#. Copy the manila-service-vm iso to the Fuel Master node:

   **Example:**

   .. code-block:: console

      # scp manila-service-image.qcow2 root@fuel-master:/tmp

#. Log into Fuel Master node CLI as root.

#. Set path to manila service image into environment variable MANILA_IMAGE

   **Example:**

   .. code-block:: console

      # export MANILA_IMAGE=/tmp/manila-service-image.qcow2

#. Install the plugin by typing:

   .. code-block:: console

      # fuel plugins --install fuel-plugin-manila-1.0-1.0.0-1.noarch.rpm

#. Verify that the plugin is installed correctly:

   .. code-block:: console

     # fuel plugins
     id | name               | version | package_version
     ---|------------     ---|---------|----------------
     1  | fuel-plugin-manila | 1.0.0   | 4.0.0


   .. raw:: latex

      \pagebreak


Uninstall Manila plugin for Fuel
--------------------------------

To uninstall Manila plugin for fuel, follow the steps below:

#. Log in to the Fuel Master node CLI

#. Delete all environments in which Manila plugin for Fuel is enabled:

   **Example:**

  .. code-block:: console

     # fuel --env <ENV_ID> env delete

3. Uninstall the plugin:

  .. code-block:: console

     # fuel --plugins --remove fuel-plugin-manila==1.0.0

4. Verify wheter the Manila plugin for Fuel was uninstalled successfully:

  .. code-block:: console

     # fuel plugins


Proceed to :ref:`pg-configure`.

.. _Fuel Plugins Catalog: https://www.mirantis.com/products/openstack-drivers-and-plugins/fuel-plugins/

   .. raw:: latex

      \pagebreak
