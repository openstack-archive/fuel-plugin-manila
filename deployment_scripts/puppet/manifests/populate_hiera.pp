notify {'MODULAR: manila/populate_hiera': }

$manila       = hiera_hash('manila', false)
$file         = '/etc/hiera/plugins/fuel-plugin-manila.yaml'
$new_password = generate("/bin/bash", "-c", "/bin/date +%s | sha256sum | base64 | head -c 32 ; echo -n")

if ! $manila {
  notify {"DBG! manila is empty. Do something ${new_npassword}": }
  populate_hiera($file, 'user_password', $new_password)
  } else {
  notify {"DBG! manila non empty. is ${manila}": }
  }
