notify {'MODULAR manila/keystone': }

$manila           = hiera_hash('manila', {})
$pass             = $manila['user_password']

$network_metadata = hiera_hash('network_metadata', {})
$public_ip        = $network_metadata['vips']['public']['ipaddr']
$admin_ip         = $network_metadata['vips']['management']['ipaddr']
$internal_ip      = $admin_ip

class {'::puppet-manila::keystone::auth':
  password        => $pass,
  public_url      => "http://${public_ip}:8786/v1/%(tenant_id)s",
  public_url_v2   => "http://${public_ip}:8786/v2/%(tenant_id)s",
  admin_url       => "http://${admin_ip}:8786/v1/%(tenant_id)s",
  admin_url_v2    => "http://${admin_ip}:8786/v2/%(tenant_id)s",
  internal_url    => "http://${internal_ip}:8786/v1/%(tenant_id)s",
  internal_url_v2 => "http://${internal_ip}:8786/v2/%(tenant_id)s",
}
