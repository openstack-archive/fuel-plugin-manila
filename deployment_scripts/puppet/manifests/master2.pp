notify {'MODULAR: fuel-plugin-manila/master2': }

file {'/tmp/manila_master2':
  ensure  => file,
  content => 'I am the file2',
}
