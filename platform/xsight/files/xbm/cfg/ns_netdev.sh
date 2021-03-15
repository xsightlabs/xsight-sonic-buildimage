#!/bin/bash

set -x

# 1. Create 4 namespaces
ip netns add h1
ip netns add h2
ip netns add h3
ip netns add h4

# 2. Create vethernet links
ip link add h1-eth1 type veth peer name veth2
ip link add h2-eth1 type veth peer name veth4
ip link add h3-eth1 type veth peer name veth6
ip link add h4-eth1 type veth peer name veth8

# 3. Move host ports into namespaces
ip link set h1-eth1 netns h1
ip link set h2-eth1 netns h2
ip link set h3-eth1 netns h3
ip link set h4-eth1 netns h4

# 4. Setup ip
ip netns exec h1 ifconfig h1-eth1 192.168.1.2/24
ip netns exec h1 ip -6 address add 2001:DB8:0:1::100/64 dev h1-eth1
ip netns exec h1 ifconfig lo up
ip netns exec h2 ifconfig h2-eth1 192.168.2.2/24
ip netns exec h2 ip -6 address add 2001:DB8:0:2::100/64 dev h2-eth1
ip netns exec h2 ifconfig lo up
ip netns exec h3 ifconfig h3-eth1 192.168.3.2/24
ip netns exec h3 ip -6 address add 2001:DB8:0:3::100/64 dev h1-eth1
ip netns exec h3 ifconfig lo up
ip netns exec h4 ifconfig h4-eth1 192.168.4.2/24
ip netns exec h4 ip -6 address add 2001:DB8:0:4::100/64 dev h2-eth1
ip netns exec h4 ifconfig lo up


sysctl net.ipv6.conf.veth0.disable_ipv6=1
sysctl net.ipv6.conf.Ethernet0.disable_ipv6=1

ifconfig veth2 up
ifconfig veth4 up
ifconfig veth6 up
ifconfig veth8 up

echo "ip netns exec h1 bash"
echo "ip netns exec h2 bash"
echo "ip netns exec h3 bash"
echo "ip netns exec h4 bash"
#ip netns exec h1 bash
#ip netns exec h2 bash
