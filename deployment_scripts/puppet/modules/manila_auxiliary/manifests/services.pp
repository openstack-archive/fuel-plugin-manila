class manila_auxiliary::services () {
  exec { 'manual_db_sync':
    command => 'manila-manage db sync',
    path    => '/usr/bin',
    user    => 'manila',
    }->
    service { 'manila-api':
      ensure    => 'running',
      name      => 'manila-api',
      enable    => true,
      hasstatus => true,
      }->
      service { 'manila-scheduler':
        ensure    => 'running',
        name      => 'manila-scheduler',
        enable    => true,
        hasstatus => true,
        }->
        service { 'manila-share':
          ensure    => 'running',
          name      => 'manila-share',
          enable    => true,
          hasstatus => true,
          }->
          service {'manila-data':
            ensure => 'running',
            name   => 'manila-data',
          }
}
