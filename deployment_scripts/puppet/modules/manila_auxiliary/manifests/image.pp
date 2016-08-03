
class manila_auxiliary::image (
  $image = 'manila-service-image.qcow2',
){
  file {'/tmp/upload_cirros.rb':
    source => 'puppet:///modules/manila_auxiliary/upload_cirros.rb',
}->

  exec {'upload-service-image':
    command => 'ruby /tmp/upload_cirros.rb',
  }
}
