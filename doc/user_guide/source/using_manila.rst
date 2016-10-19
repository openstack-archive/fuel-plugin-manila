Using File Share as a Service possibility with Manila plugin for Fuel
---------------------------------------------------------------------

Once you deploy an OpenStack environment with Manila plugin for Fuel, you can
start using it both from CLI and Horizon. The topic of CLI usage is too big to
put it into this User Guide and it well described `here
<http://docs.openstack.org/cli-reference/manila.html>`_.

The Horizon usage is very obvious. You can notice that two new tabs are reveals
on the Admin and Project/Compute sections:

   .. figure:: static/admin.png
      :width: 90%

   .. raw:: latex

      \pagebreak

   .. figure:: static/project.png
      :width: 90%

   .. raw:: latex

      \pagebreak

Let's go over the basic usage of Manila:

#. Firstly we have to create a share network for access to new share:

   .. figure:: static/create_network.png
      :width: 75%

   .. raw:: latex

      \pagebreak

#. After that we can create new share:

   .. figure:: static/create_share.png
      :width: 75%

   .. raw:: latex

      \pagebreak

3. When the share becomes available it should be configured for future usage.
At least necessary to add new rule in order to allow mounting new share.

   .. figure:: static/edit_share.png
      :width: 90%

   .. figure:: static/add_rule.png
      :width: 90%

After that new share could be consumed in your environment.

   .. raw:: latex

      \pagebreak
