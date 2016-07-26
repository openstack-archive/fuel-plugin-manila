notify {'MODULAR: fuel-plugin-manila/install': }

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

Package['python-pip']->Package['pycrypto']->Package['python-manila']->Package['python-manilaclient']->Package['python-manila-ui']
