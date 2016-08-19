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

package {'python-pymysql':
  ensure => 'installed'
}

package {'python-pip':
  ensure => 'installed'
}

package {'python-dev':
  ensure => 'installed'
}

package {'pycrypto':
  ensure => 'installed',
  provider => 'pip',
}

package {'python-manila':
  ensure => 'installed'
}

class {'::manila_auxiliary::fs': }

create_resources('::manila_auxiliary::initd', $inits)

Package['python-pip']->Package['python-dev']->Package['pycrypto']->Package['python-manila']
