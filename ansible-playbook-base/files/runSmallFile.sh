#!/bin/bash

run_smallfile()
{
	cd /tmp/gbench/smallfile
	case "$1" in
        create)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation create --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 1000 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        append)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation append --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 1000 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        read)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation read --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 1000 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        rename)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation rename --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 1000 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        mkdir)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation mkdir --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 1000 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        rmdir)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation rmdir --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 1000 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        delete-renamed)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation delete-renamed --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 1000 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        ls-l)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation ls-l --threads 4  --file-size 64 --files $2 --response-times Y --top /mnt/bricks/fsgbench0001 --pause 500 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
        cleanup)
            python /tmp/gbench/smallfile/smallfile_cli.py --operation ls-l --threads 4  --response-times Y --top /mnt/bricks/fsgbench0001 --pause 500 --host-set "`echo $CLIENT | tr ' ' ','`"
            ;;
	esac
}

source=${BASH_SOURCE[0]}
	if [ $source == $0 ]; then
		run_smallfile $1 $2
	fi

