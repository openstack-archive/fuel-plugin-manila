"""Copyright 2016 Mirantis, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

import os

from fuelweb_test.helpers import utils

from proboscis.asserts import assert_true

from settings import MANILA_PLUGIN_PATH
from settings import plugin_name


# constant
msg = "Plugin couldn't be enabled. Check plugin version. Test aborted"


def install_manila_plugin(master_node_ip):
    """Install plugin packages to the master node."""
    utils.upload_tarball(
        master_node_ip,
        MANILA_PLUGIN_PATH, "/var")
    utils.install_plugin_check_code(
        master_node_ip,
        os.path.basename(MANILA_PLUGIN_PATH))


def enable_plugin_manila(cluster_id, fuel_web_client):
    """Enable Manila plugin on cluster."""
    assert_true(
        fuel_web_client.check_plugin_exists(
            cluster_id, plugin_name),
        msg)
    options = {'metadata/enabled': True}
    fuel_web_client.update_plugin_data(cluster_id, plugin_name, options)


def disable_plugin_manila(cluster_id, fuel_web_client):
    """Disable Manila plugin on cluster."""
    assert_true(
        fuel_web_client.check_plugin_exists(
            cluster_id, plugin_name),
        msg)
    options = {'metadata/enabled': False}
    fuel_web_client.update_plugin_data(cluster_id, plugin_name, options)
