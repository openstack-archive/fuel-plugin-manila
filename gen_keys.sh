#!/bin/sh

CLUSTER_ID=$1

if [ ! -d /var/lib/fuel/keys/$CLUSTER_ID/manila ]; then
    sh /etc/puppet/modules/osnailyfacter/modular/astute/generate_keys.sh -p /var/lib/fuel/keys/ -i $CLUSTER_ID -s 'manila'
fi
