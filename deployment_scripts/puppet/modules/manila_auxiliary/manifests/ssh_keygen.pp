class manila_auxiliary::ssh_keygen (
  $name = '/root/.ssh/id_rsa',
  $user = 'root',
) {
  exec {'manila_ssh_keygen':
    command => "ssh-keygen -t rsa -f ${name} -N ''",
    user    => $user,
    path    => '/bin:/usr/bin',
  }
}
