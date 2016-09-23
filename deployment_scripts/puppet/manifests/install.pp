notify {'MODULAR: fuel-plugin-manila/install': }

package {'python-pip':
  ensure => 'installed'
}

package {'python-pymysql':
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

package {'python-manilaclient':
  ensure => 'installed'
}

package {'python-manila-ui':
  ensure => 'installed'
}

class {'::manila_auxiliary::fs': }

file {'/etc/apt/preferences.d/fuel-plugin-manila.pref':
  source => 'puppet:///modules/manila_auxiliary/fuel-plugin-manila.pref',
  owner  => 'root',
  group  => 'root'
}

class {'::apt::update': }


Package['python-pip']->
Package['python-dev']->
Package['python-pymysql']->
Package['pycrypto']->
File['/etc/apt/preferences.d/fuel-plugin-manila.pref']->
Class['::apt::update']->
Package['python-manila']->
Package['python-manilaclient']->
Package['python-manila-ui']
