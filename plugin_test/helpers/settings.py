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
MANILA_PLUGIN_VERSION = os.environ.get('MANILA_PLUGIN_VERSION')
MANILA_PLUGIN_PATH = os.environ.get('MANILA_PLUGIN_PATH')
MANILA_IMAGE_PATH = os.environ.get('MANILA_IMAGE_PATH')
plugin_name = 'fuel-plugin-manila'
