notify {'MODULAR: fuel-plugin-manila/populate_hiera': }

$manila       = hiera_hash('manila', false)
$file         = '/etc/hiera/plugins/fuel-plugin-manila.yaml'
$new_password = generate("/bin/bash", "-c", "/bin/date +%s | sha256sum | base64 | head -c 32 ; echo -n")
$db_password  = generate("/bin/bash", "-c", "/bin/date +%s | sha256sum | base64 | head -c 32 ; echo -n")

if ! $manila {
  populate_hiera($file, 'user_password', $new_password)
  populate_hiera($file, 'db_password', $db_password)
  }
