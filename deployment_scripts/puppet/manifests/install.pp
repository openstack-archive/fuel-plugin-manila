notify {'MODULAR: fuel-plugin-manila/install': }

$manila = hiera_hash('fuel-plugin-manila', {})
$image  = $manila['fuel-plugin-manila_image']

$master_ip = hiera('master_ip')
$src_image = "http://${master_ip}:8080/plugins/fuel-plugin-manila-1.0/repositories/ubuntu/${image}"
$inits = {
  'manila-api' => {
    desc => 'manila-api init',
    srv  => 'manila-api',},
  'manila-share' => {
    desc => 'manila-share init',
    srv  => 'manila-share',},
  'manila-data' =>{
    desc => 'manila-data init',
    srv  => 'manila-data',},
  'manila-scheduler' => {
    desc => 'manila-scheduler init',
    srv  => 'manila-scheduler',},
}

package {'python-pip':
  ensure => 'installed'
}

package {'pycrypto':
  ensure => 'installed',
  provider => 'pip',
}

package {'python-manila':
  ensure => 'installed'
}

package {'python-manilaclient':
  ensure => 'installed'
}

package {'python-manila-ui':
  ensure => 'installed'
}

class {'::manila_auxiliary::fs': }

create_resources('::manila_auxiliary::initd', $inits)

class {'::manila_auxiliary::image':
  src_image => $src_image,
  image     => $image,
}

class {'::manila_auxiliary::ssh_keygen': }

Package['python-pip']->Package['pycrypto']->Package['python-manila']->Package['python-manilaclient']->Package['python-manila-ui']
