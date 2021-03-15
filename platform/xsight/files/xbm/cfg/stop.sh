#!/bin/bash

echo ">>> Removing tuntap devices"

# Down CPU port
ip link set dev xcpu down
ip link set dev veth0 down
ip link del dev veth0 type veth peer name xcpu

#ip link del dev veth2
#ip link del dev veth4
#ip link del dev veth6
#ip link del dev veth8

# Setup front panel ports
#num_ports=4
#for i in `seq 1 ${num_ports}`
#do
#    ip link set swp${i} down
#    ip tuntap del dev swp${i} mode tap
#done

#echo ">>> Configuring bridge"
#ip link set v100 down
#brctl delbr v100

echo ">>> Del routes"
#ip route del 192.168.101.0/24 nexthop via 192.168.4.2
#ip route del 192.168.102.0/24 nexthop via 192.168.4.2 nexthop via 192.168.4.3
#ip route del default via 192.168.1.1 dev Ethernet0
#ip route del default via 192.168.2.1 dev Ethernet1

#ip netns del h1
#ip netns del h2
#ip netns del h3
#ip netns del h4

# ip route del 3ffe:2::/64 nexthop via 2ffe:4::2
# ip route del 3ffe:3::/64 nexthop via 2ffe:4::2 nexthop via 2ffe:4::3

echo ">>> Interfaces"
ifconfig
echo ">>> Routes"
ip ro
echo ">>> Neighbors"
ip neigh


