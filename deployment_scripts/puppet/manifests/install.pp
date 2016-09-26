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

package {'fuel-plugin-manila-manila-core':
  ensure => 'installed'
}

package {'fuel-plugin-manila-manilaclient':
  ensure => 'installed'
}

package {'fuel-plugin-manila-manila-ui':
  ensure => 'installed'
}

class {'::manila_auxiliary::fs': }

Package['python-pip']->
Package['python-dev']->
Package['python-pymysql']->
Package['pycrypto']->
Package['fuel-plugin-manila-manila-core']->
Package['fuel-plugin-manila-manilaclient']->
Package['fuel-plugin-manila-manila-ui']
