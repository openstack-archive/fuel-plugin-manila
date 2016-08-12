class manila_auxiliary::ui () {

  include ::apache::params
  include ::apache::service

  $adm_shares  = '/usr/lib/python2.7/dist-packages/manila_ui/enabled'
  $hor_enabled = '/usr/share/openstack-dashboard/openstack_dashboard/enabled/'

  exec {'add_share_panel':
    command => "cp ${adm_shares}/_90*.py ${hor_enabled}",
    path    => '/bin:/usr/bin',
  }

  Exec['add_share_panel'] ~> Service['httpd']
}
