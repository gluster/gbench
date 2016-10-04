#!/bin/bash

run_drop_cache()
{
    for host in $SERVERS $CLIENTS
    do
        ssh root@${host} echo "Dropping cache on $host"
        ssh root@${host} sync
        ssh root@${host} "echo 3 > /proc/sys/vm/drop_caches"
    done
}

source=${BASH_SOURCE[0]}
    if [ $source == $0 ]; then
        run_drop_cache
    fi
