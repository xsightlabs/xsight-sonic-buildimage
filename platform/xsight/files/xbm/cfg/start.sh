#!/bin/bash

#echo ">>> Configuring namespaces"
#read -p "--- Press enter to continue ---"
#/home/admin/xbm/cfg/ns_netdev.sh

#echo ">>> Starting VETH pairs"
#/home/admin/xbm/cfg/up_veth_ifs.sh
#sleep 3

echo ">>> Start XBM"
#read -p "--- Press enter to continue ---"
#read -p '---- Please run XBM ---'
rm -f /home/admin/xbm/log/*
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

