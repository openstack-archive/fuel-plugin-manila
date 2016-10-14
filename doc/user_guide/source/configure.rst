.. _pg-configure:

Configure Manila plugin for Fuel
--------------------------------

Configuring and deploying an environment with Manila plugin for Fuel involves
creating an environment in Fuel and modifying the environment settings.

**To configure OpenStack environment with Manila plugin:**

#. Create an OpenStack environment as described in the `Fuel User Guide <http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/create-environment.html>`_:

#. In the :guilabel:`Additional services` menu, select :guilabel:`Install Manila`:

   .. figure:: static/additional.png
      :width: 90%

   .. raw:: latex

      \pagebreak

#. Follow next steps of the `Create a new OpenStack
   environment <http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/create-environment/start-create-env.html>`_
instruction.

#. In the :guilabel:`Nodes` tab of the Fuel web UI `add
   <http://docs.openstack.org/developer/fuel-docs/userdocs/fuel-user-guide/configure-environment/add-nodes.html>`_
   at least one node with roles manila-share and manila-data:

   .. figure:: static/nodes.png
      :width: 90%

   .. raw:: latex

      \pagebreak

#. In the :guilabel:`Settings` tab, click :guilabel:`OpenStack Serivces`:

   #. Check that :guilabel:`Enable Manila service` is enabled.
   #. Set the choosend backend for Manila.

      #. For generic driver specify the :guilabel:`Image name` exactly same as
         you set on the plugin installation stage.
      #. For NetApp driver specify hostname, credential and parameters related
         to your environment.

   .. figure:: static/config.png
      :width: 90%

   .. raw:: latex

      \pagebreak
