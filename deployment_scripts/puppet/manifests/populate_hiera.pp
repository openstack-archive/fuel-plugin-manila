notify {'MODULAR: fuel-plugin-manila/populate_hiera': }

$manila        = hiera_hash('manila', {})
$fpg_manila    = hiera_hash('fuel-plugin-manila', {})

$file          = '/etc/hiera/plugins/fuel-plugin-manila.yaml'
$new_password  = generate("/bin/bash", "-c", "/bin/date +%s | sha256sum | base64 | head -c 32 ; echo -n")
sleep 1
$db_password   = generate("/bin/bash", "-c", "/bin/date +%s | sha256sum | base64 | head -c 32 ; echo -n")

$image_name    = 'manila-service-image'
$service_image = $fpg_manila['fuel-plugin-manila_image']
$img_data      = {
  container_format  => 'bare',
  disk_format       => 'qcow2',
  glance_properties => '',
  img_name          => $image_name,
  img_path          => "/tmp/${service_image}",
  min_ram           => 256,
  os_name           => 'ubuntu',
  public            => 'true',
}

if ! $manila {
  populate_hiera($file, 'user_password', $new_password)
  populate_hiera($file, 'db_password', $db_password)
  populate_hiera($file, 'service_vm_image', $img_data)
  }
