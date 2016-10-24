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

        run_drop_cache
