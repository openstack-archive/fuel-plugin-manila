notify {'MODULAR: fuel-plugin-manila/install': }

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

class{'::manila_auxiliary::fs': }

create_resources('::manila_auxiliary::initd', $inits)

Package['python-pip']->Package['pycrypto']->Package['python-manila']->Package['python-manilaclient']->Package['python-manila-ui']
