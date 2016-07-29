class manila_auxiliary::fs () {
  file {'/etc/manila':
    ensure => 'directory',
  }->
  file {'/etc/manila/rootwrap.d':
    ensure => 'directory',
  }
  file { '/var/log/manila':
    ensure => 'directory',
  }
  file {'/etc/manila/api-paste.ini':
    source => "puppet:///modules/manila_auxiliary/api-paste.ini",
  }
  file {'/etc/manila/logging_sample.conf':
    source => "puppet:///modules/manila_auxiliary/logging_sample.conf",
  }
  file {'/etc/manila/policy.json':
    source => "puppet:///modules/manila_auxiliary/policy.json",
  }
  file {'/etc/manila/rootwrap.conf':
    source => "puppet:///modules/manila_auxiliary/rootwrap.conf",
  }
  file {'/etc/manila/rootwrap.d/share.filters':
    source => "puppet:///modules/manila_auxiliary/share.filters"
  }
}
