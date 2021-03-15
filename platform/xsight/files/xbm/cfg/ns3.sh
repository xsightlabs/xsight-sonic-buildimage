#!/bin/bash

#ip ro add 192.168.1.0/24 via 192.168.2.1
ip ro add default via 192.168.3.1 dev h3-eth1
ip -6 ro add 2001:db8:0:1::/64 via 2001:db8:0:1::1
ip -6 ro add 2001:db8:0:2::/64 via 2001:db8:0:2::1
ip -6 ro add 2001:db8:0:4::/64 via 2001:db8:0:4::1
#/usr/sbin/sshd -o PidFile=/run/sshd-h2.pid
ethtool --offload  h3-eth1  rx off  tx off
sett H3

echo '--- Exsiting routes---'
ip ro
ip -6 ro
