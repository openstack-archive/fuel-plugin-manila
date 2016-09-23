#!/bin/sh

CLUSTER_ID=$1
PLUGIN_YAML=/etc/fuel/cluster/$CLUSTER_ID/fuel-plugin-manila.yaml

if [ ! -f $PLUGIN_YAML ]; then

    gen_pass() {
	openssl rand -base64 32|tr -d '='
    }

    user_pass=$(gen_pass)
    maniladb_pass=$(gen_pass)

    echo "
---
  manila:
    user_password: $user_pass
    db_password: $maniladb_pass
    service_vm_image:
      container_format: bare
      disk_format: qcow2
      glance_properties: \"\"
      img_name: manila-service-image
      img_path: /tmp/manila-service-image.qcow2
      min_ram: \"256\"
      os_name: ubuntu
      public: \"true\"
" > $PLUGIN_YAML
fi
