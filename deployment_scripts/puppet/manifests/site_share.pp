#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

notify {'MODULAR: fuel-plugin-manila/site_share': }

$manila      = hiera_hash('manila', {})
$db_user     = 'manila'
$db_pass     = $manila['db_password']
$manila_pass = $manila['user_password']
$db_host     = hiera('database_vip')
$sql_conn    = "mysql+pymysql://${db_user}:${db_pass}@${db_host}/manila?charset=utf8"
$image       = $manila['service_vm_image']['img_name']

$rabbit_hash   = hiera_hash('rabbit', {})
$amqp_user     = $rabbit_hash['user']
$amqp_password = $rabbit_hash['password']
$amqp_hosts    = split(hiera('amqp_hosts', ''), ',')

$network_metadata = hiera_hash('network_metadata', {})
$ns               = hiera_hash('network_scheme', {})
$mgmt_ip          = $network_metadata['vips']['management']['ipaddr']
$br_mgmt          = split($ns['endpoints']['br-mgmt']['IP'][0], '/')
$br_mgmt_ip       = $br_mgmt[0]


$neutron       = hiera_hash('quantum_settings', {})
$neutron_pass  = $neutron['keystone']['admin_password']
$auth_url      = "http://${mgmt_ip}:35357/"
$auth_uri      = "http://${mgmt_ip}:5000/"

$cinder        = hiera_hash('cinder', {})
$cinder_pass   = $cinder['user_password']

$nova          = hiera_hash('nova', {})
$nova_pass     = $nova['user_password']

$verbose       = hiera('verbose')
$debug         = hiera('debug')
$use_syslog    = hiera('use_syslog')


$backends = {'generic' =>
  {'share_backend_name'            => 'generic',
    'driver_handles_share_servers' => 'true',
    'share_driver'                 => 'manila.share.drivers.generic.GenericShareDriver',
    'service_instance_user'        => 'manila',
    'service_instance_password'    => 'manila',
    'service_image_name'           => $image,
    'path_to_private_key'          => '/var/lib/astute/manila/manila',
    'path_to_public_key'           => '/var/lib/astute/manila/manila.pub',
  }
}


class {'::manila_auxiliary':
  sql_connection      => $sql_conn,
  shared_backends     => 'generic', #should be array of backends
  amqp_durable_queues => 'False',
  rabbit_userid       => $amqp_user,
  rabbit_hosts        => $amqp_hosts,
  rabbit_use_ssl      => 'False',
  rabbit_password     => $amqp_password,
  auth_url            => $auth_url,
  auth_uri            => $auth_uri,
  br_mgmt_ip          => $br_mgmt_ip,
  cinder_pass         => $cinder_pass,
  manila_pass         => $manila_pass,
  neutron_pass        => $neutron_pass,
  nova_pass           => $nova_pass,
  verbose             => $verbose,
  debug               => $debug,
}->


class {'::manila_auxiliary::services': }

Class['::manila_auxiliary']->
Class['::manila_auxiliary::services']


create_resources('::manila_auxiliary::backend::generic', $backends)
