notify {'MODULAR: fuel-plugin-manila/install': }

$master_ip             = hiera('master_ip')
$manilaclient_pkg_name = 'fuel-plugin-manila-manilaclient'
$manilaclient_pkg      = "${manilaclient_pkg_name}_1.8.2_all.deb"
$manilaclient_pkg_url  = "http://${master_ip}:8080/plugins/fuel-plugin-manila-1.0/repositories/ubuntu/${manilaclient_pkg}"

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

exec { 'install_manilaclient':
  path    => '/usr/sbin:/usr/bin:/sbin:/bin:',
  command => "wget ${manilaclient_pkg_url} -O /tmp/${manilaclient_pkg} && dpkg --force-overwrite -i /tmp/${manilaclient_pkg}",
  onlyif  => "echo \"! dpkg -l ${manilaclient_pkg_name}\" | bash",
}


package {'python-manila':
  ensure => 'absent'
}

package {'manila-api':
  ensure => 'absent'
}

package {'manila-common':
  ensure => 'absent'
}

package {'manila-scheduler':
  ensure => 'absent'
}

package {'fuel-plugin-manila-manila-core':
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
Package['python-manila']->
Package['manila-api']->
Package['manila-common']->
Package['manila-scheduler']->
Package['fuel-plugin-manila-manila-core']->
Exec['install_manilaclient']->
Package['fuel-plugin-manila-manila-ui']
