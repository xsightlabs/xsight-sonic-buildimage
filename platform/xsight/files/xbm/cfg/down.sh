#!/bin/bash

echo ">>> Down front panel ports"
num_ports=3
for i in `seq 0 ${num_ports}`
do
    ip link set Ethernet${i} down
done

echo ">>> Down VETH pairs"
/home/admin/xbm/cfg/down_veth_ifs.sh

#echo ">>> Down CPU port"
#ip link set Ethernet0 down

#echo ">>> Interfaces"
#ip link | grep Ethernet
