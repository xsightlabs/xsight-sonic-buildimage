#!/bin/bash

echo ">>> Configuring CPU port VETH devices"

# Setup CPU port
ip link add name veth0 type veth peer name xcpu
ip link set dev veth0 up
ip link set dev xcpu up

echo ">>> Re-load NetDev"
#read -p "--- Press enter to continue ---"
/home/admin/xbm/cfg/xrm.sh
/home/admin/xbm/cfg/xload.sh

echo ">>> Sleeping 5"
sleep 5

echo ">>> Set XPCI debug level to INFO(3)"
echo 3 > /proc/sys/dev/xpci_dev/debug_level

#echo ">>> Configuring namespaces"
#read -p "--- Press enter to continue ---"
#/home/admin/xbm/cfg/ns_netdev.sh

#echo ">>> Starting VETH pairs"
#/home/admin/xbm/cfg/up_veth_ifs.sh
#sleep 3

echo ">>> Start XBM"
#read -p "--- Press enter to continue ---"
#read -p '---- Please run XBM ---'
#rm -f /home/admin/xbm/log/*
/home/admin/xbm/cfg/run_xbm.sh&
#sleep 30

echo ">>> Sleeping 10"
sleep 10

echo ">>> Interfaces"
ip link
echo ">>> Routes"
ip ro
echo ">>> Neighbors"
ip neigh

#echo ">>> Down all interfaces"
#read -p "--- Press enter to continue ---"
#/home/admin/xbm/cfg/down_netdev.sh

#echo ">>> Start SwitchLink"
#source xs_sai_env.sh
#read -p "--- Press enter to continue ---"
#../bin/xswlink --sai-only&

#read -p "--- Press enter till SwitchLink is READY ---"

#echo ">>> Init interfaces"
#/home/admin/xbm/cfg/init_rtnl.sh

#read -p "--- Press enter to continue ---"
#/home/admin/xbm/cfg/cfg_netdev.sh

