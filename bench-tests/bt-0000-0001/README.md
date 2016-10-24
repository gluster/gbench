# Benchmark test 0000-0001

This benchmark test uses IOZone [1] and smallfile [2] test suites to test various
performance charecteristics of Gluster.

The tests that are run using IOZone are, sequential write, sequential read,
random read/write.

The tests that are run using smallfile are, create, read, ls -l (listing)

## Pre-requisites
  - The environment variable CLIENTS must be set and contain a space separated
    list of IPs or hostnames [a]
  - The environment variable SERVERS must be set and contain a space separated
    list of IPs or hostnames [b]
  - The smallfile application must be installed in /root/smallfile. If you have git installed this step will be performed during execution.
  - Passwordless SSH should be setup across the CLIENTS and SERVERS [c]
  - Provided sync-drop-caches.sh should be copied to /root/sync-drop-caches.sh
  
[a] To set the env. variable temporarily for the current shell and all the processes started from the current shell:

``` export CLIENTS=your-client-ip-01\ your-client-ip-02 #Space seperated list of IPs ```

[b] To set the env. variable temporarily for the current shell and all the processes started from the current shell:

``` export SERVERS=your-server-ip-01\ your-server-ip-02  #Space seperated list of IPs ```
  
[c] To check the same, try ``` ssh root@yourclient_ip ```. 
If you're able to access root@yourclient_ip without the root password, you're all set.

## Arguments to the test tool

```
-s <size in KB>
        Record size for IOZone runs
        File size for the smallfile tests
        The same value is used for both series of tests
-f <files>
        Number of small files to create per smallfile test thread
        (default threads 8)
-n <number of samples>
        This setting runs a test multiple times (i.e collecting as many samples
        as requested), and provides an average across the runs. IOW, it enables
        collecting multiple test data, to avoid any noise in the test reflecting
        in the results.
-m <mount point>
        Specifies the location where a gluster volume is mounted.

Example: GlusterBench.py -s 64 -f 10000 -n 5 -m storage-pool -v
```

## Sample output
```
Gluster Benchmark Kit report for 07:10:23
Sequential Writes 64 record size: 1922003
Sequential Reads  64 record size: 2480545
Random Writes     64 record size: 295288
Random Reads      64 record size: 477069
Smallfile Creates 64   file size: 3015
Smallfile Reads   64   file size: 3128
Smallfile ls -l   64   file size: 31256
```

## Links and references

[1] http://www.iozone.org/

[2] https://github.com/bengland2/smallfile
