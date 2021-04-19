#!/bin/bash

echo ">>> Start XBM"
#read -p "--- Press enter to continue ---"
#read -p '---- Please run XBM ---'
rm -f /home/admin/xbm/log/*
/home/admin/xbm/cfg/run_xbm.sh&

echo ">>> Sleeping 10"
sleep 10

echo ">>> Interfaces"
ip link
echo ">>> Routes"
ip ro
echo ">>> Neighbors"
ip neigh
