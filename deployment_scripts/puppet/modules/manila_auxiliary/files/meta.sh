#!/bin/bash

. /root/openrc

if ! openstack --insecure flavor list | grep -q 'manila-service-flavor'; then
    echo 'add manila-service-flavor'
    openstack --insecure flavor create manila-service-flavor \
      --id 100  \
      --ram 256 \
      --disk 0  \
      --vcpus 1
fi

if ! manila --insecure type-list | grep -q 'default_share_type'; then
     echo 'add default_share_type'
     manila type-create default_share_type True
 fi
