#!/bin/bash

yum install -y opensm
service opensm start
yum groupinstall -y "Infiniband Support"
#yum install -y glusterfs-rdma
chkconfig rdma on
service rdma start
echo "DEVICE=${1}" > /etc/sysconfig/network-scripts/ifcfg-ib0
echo "BOOTPROTO=none" >> /etc/sysconfig/network-scripts/ifcfg-ib0
echo "ONBOOT=yes" >> /etc/sysconfig/network-scripts/ifcfg-ib0
echo "TYPE=Infiniband" >> /etc/sysconfig/network-scripts/ifcfg-ib0
echo "NETMASK=${2}" >> /etc/sysconfig/network-scripts/ifcfg-ib0
echo "IPADDR=${3}" >> /etc/sysconfig/network-scripts/ifcfg-ib0
echo "GATEWAYDEV=${4}" >> /etc/sysconfig/network
service network restart
