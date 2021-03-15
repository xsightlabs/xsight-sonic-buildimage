#!/bin/bash

echo ">>> Add interface IP addresses"

ip address add 192.168.1.1/24 dev Ethernet0
#ip -6 address add 2001:DB8:0:1::1/64 dev Ethernet0
ip address add 192.168.2.1/24 dev Ethernet1
#ip -6 address add 2001:DB8:0:2::1/64 dev Ethernet1
ip address add 192.168.3.1/24 dev Ethernet2
#ip -6 address add 2001:DB8:0:3::1/64 dev Ethernet2
ip address add 192.168.4.1/24 dev Ethernet3
#ip -6 address add 2001:DB8:0:4::1/64 dev Ethernet3

echo ">>> Interfaces"
ip link | grep Ethernet
echo ">>> Routes"
ip ro
echo ">>> Neighbors"
ip neigh
