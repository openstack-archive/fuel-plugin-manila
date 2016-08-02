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

notify {'MOUDULAR: fuel-plugin-manila/site': }

$manila        = hiera_hash('manila', {})
$db_user       = 'manila'
$db_pass       = $manila['db_password']
$db_host       = hiera('database_vip')
$sql_conn      = "mysql+pymysql://${db_user}:${db_pass}@${db_host}/manila?charset=utf8"

$rabbit_hash   = hiera_hash('rabbit', {})
$amqp_user     = $rabbit_hash['user']
$amqp_password = $rabbit_hash['password']
$amqp_hosts    = split(hiera('amqp_hosts', ''), ',')

$network_metadata = hiera_hash('network_metadata', {})
$mgmt_ip          = $network_metadata['vips']['management']['ipaddr']

$verbose       = hiera('verbose')
$debug         = hiera('debug')
$use_syslog    = hiera('use_syslog')

$neutron       = hiera_hash('quantum_settings', {})
$neutron_pass  = $neutron['keystone']['admin_password']
$neutron_url   = "http://${mgmt_ip}:35357/"

$cinder        = hiera_hash('cinder', {})
$cinder_pass   = $cinder['user_password']
$auth_url      = "http://${mgmt_ip}:35357/"

$nova          = hiera_hash('nova', {})
$nova_pass     = $nova['user_password']

class {'::manila':
  sql_connection  => $sql_conn,
  rabbit_userid   => $amqp_user,
  rabbit_hosts    => $amqp_hosts,
  rabbit_password => $amqp_password,
  package_ensure  => 'absent',
  verbose         => $verbose,
  debug           => $debug,
  use_syslog      => $use_syslog,
  log_facility    => 'LOG_LOCAL4',
}

class {'::manila::quota':
}

class {'::manila::network::neutron':
  neutron_admin_password => $neutron_pass,
  neutron_admin_auth_url => $neutron_url,
}

class {'::manila::volume::cinder':
  cinder_admin_password => $cinder_pass,
  cinder_admin_auth_url => $auth_url,
}

class {'::manila::compute::nova':
  nova_admin_password => $nova_pass,
  nova_admin_auth_url => $auth_url,
}

class {'::manila::backends':
  enabled_share_backends => ['generic'],
}

$gen = {'generic' =>
  {'share_backend_name' => 'generic',
    'driver_handles_share_servers' => 'true',
  }
}

create_resources('::manila::backend::generic', $gen)

exec { 'manual_db_sync':
  command => $::manila::params::db_sync_command,
  path    => '/usr/bin',
  user    => 'manila',
  }->
class {'::manila::api':
  keystone_password  => $manila['user_password'],
  keystone_auth_host => $mgmt_ip,
  package_ensure     => 'absent',
  enabled            => true,
  manage_service     => true,
}

class {'::manila::scheduler':
  scheduler_driver => 'manila.scheduler.drivers.filter.FilterScheduler',
  package_ensure   => 'absent',
  enabled          => true,
  manage_service   => true,
}

class {'::manila::share':
  package_ensure => 'absent',
  enabled        => true,
  manage_service => true,
}
