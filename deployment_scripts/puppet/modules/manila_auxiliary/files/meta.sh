#!/bin/bash

. /root/openrc

if ! openstack flavor list | grep -q 'manila-service-flavor'; then
    echo 'add manila-service-flavor'
    openstack flavor create manila-service-flavor \
      --id 100  \
      --ram 256 \
      --disk 0  \
      --vcpus 1
fi
