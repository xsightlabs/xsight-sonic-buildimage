#!/bin/bash

PORT_NUM=16
ATTACH_IF="xcpu"
DEBUG_LEVEL=3
NETDEV_MODE=1
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`

echo ">>> Configuring CPU port VETH devices"

# Setup CPU port
ip link add name veth0 type veth peer name xcpu
ip link set dev veth0 up
ip link set dev xcpu up

echo ">>> Re-load NetDev"
#read -p "--- Press enter to continue ---"
rmmod xpci
# TODO: change insmod to modprobe after moving xdrivers build into sonic-buildimage
# TODO: replace attach_if=xcpu with real management port for X1
# debug_level = 1 - Error
#               2 - Notice
#               3 - Info
#               4 - Debug
#               5 - Debug with Packet trace
insmod /home/admin/xbm/cfg/xpci.ko attach_if=${ATTACH_IF} num_of_ports=${PORT_NUM} debug_level=${DEBUG_LEVEL} netdev_mode=${NETDEV_MODE}

echo ">>> Sleeping 5"
sleep 5

#echo ">>> Set XPCI debug level to INFO(3)"
#echo ${DEBUG_LEVEL} > /proc/sys/dev/xpci_dev/debug_level

if [[ ${ONIE_MACHINE} == *"kvm"* ]]; then
    echo ">>> Simulation mode. Use xbm!"
    touch /etc/sonic/use_xbm
    /home/admin/xbm/cfg/start.sh
fi

