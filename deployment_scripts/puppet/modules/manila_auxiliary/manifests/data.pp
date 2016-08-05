class manila_auxiliary::data () {
  service {'manila-data':
    ensure => ''running,
    name   => 'manila-data',
}
}
