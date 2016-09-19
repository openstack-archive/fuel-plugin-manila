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
import traceback


from fuelweb_test.helpers.ssh_manager import SSHManager
from fuelweb_test.helpers import utils
from fuelweb_test import logger

from proboscis.asserts import assert_true
from settings import MANILA_IMAGE_PATH
from settings import MANILA_PLUGIN_PATH
from settings import MANILA_IMAGE_DEST_PATH
from settings import plugin_name


def install_manila_plugin(master_node_ip):
    """Install plugin packages to the master node."""

    utils.upload_tarball(
        master_node_ip,
        MANILA_PLUGIN_PATH, "/var")
    utils.install_plugin_check_code(
        master_node_ip,
        os.path.basename(MANILA_PLUGIN_PATH))


def upload_manila_image(master_node_ip, image_dest_path=MANILA_IMAGE_DEST_PATH):
    """Copy Manila qcow2 image to the master node.

    :type master_node_ip: string master-node ip
    :type image_dest_path: string destination path
    """

    logger.info(image_dest_path)
    try:
        logger.info("Start to upload manila image file")
        SSHManager().upload_to_remote(
            ip=master_node_ip,
            source=MANILA_IMAGE_PATH,
            target=image_dest_path
        )

        manila_image_name = MANILA_IMAGE_PATH.split('/')
        dest_path = '{0}/{1}'.format(
            image_dest_path, manila_image_name[-1])
        logger.info('File {} was uploaded on master'.format(dest_path))
        return dest_path

    except Exception:
        logger.error('Failed to upload file')
        logger.error(traceback.format_exc())
        return False


def enable_plugin_manila(cluster_id, fuel_web_client, driver='generic',
                         **kwargs):
    """Enable Manila plugin on cluster."""
    assert_true(
        fuel_web_client.check_plugin_exists(cluster_id, plugin_name),
        "Plugin couldn't be enabled. Check plugin version.")
    if driver == 'generic':
        options = {'metadata/enabled': True, 'use-generic-driver/value': True}
        for name, value in kwargs.items():
            options[name] = value
        fuel_web_client.update_plugin_data(cluster_id, plugin_name, options)

    if driver == 'nettapp':
        options = {'metadata/enabled': True, 'use-netapp-driver/value': True}
        for name, value in kwargs.items():
            options[name] = value
        fuel_web_client.update_plugin_data(cluster_id, plugin_name, options)

    else:
        logger.warn("Non of drivers wasn't enabled check plugin settings")


def disable_plugin_manila(cluster_id, fuel_web_client):
    """Disable Manila plugin on cluster."""
    assert_true(
        fuel_web_client.check_plugin_exists(cluster_id, plugin_name),
        "Plugin couldn't be enabled. Check plugin version.")
    options = {'metadata/enabled': False}
    fuel_web_client.update_plugin_data(cluster_id, plugin_name, options)

