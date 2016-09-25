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

Package['python-pip']->
Package['python-dev']->
Package['python-pymysql']->
Package['pycrypto']->
Package['python-manila']->
Package['python-manilaclient']->
Package['python-manila-ui']
