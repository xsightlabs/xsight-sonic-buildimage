#!/bin/bash

USE_XBM=true
ATTACH_IF="xcpu"
PORT_NUM=32
DEBUG_LEVEL=3
NETDEV_MODE=1
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`
CFG_FILE="/home/admin/x1/hw.cfg"

function get_hw_params {
    if [[ ! -f ${CFG_FILE} ]]; then
        echo ">>> ERROR! Config file not found: ${CFG_FILE}"
        exit 1
    fi

    SYS_MODE=`sed -n -e 's/^.*sys_mode[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
    XPCI_NETDEV=`sed -n -e 's/^.*xpci_netdev[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
}

#remove use_xbm flag file before examine simulation mode
rm -f /etc/sonic/use_xbm

if [[ ${ONIE_MACHINE} == *"kvm"* ]]; then
    echo ">>> Configuring CPU port VETH devices"
    # Setup CPU port
    ip link add name veth0 type veth peer name xcpu
    ip link set dev veth0 up
    ip link set dev xcpu up
else
    get_hw_params
    if [[ ${SYS_MODE} == "asic" ]]; then
        USE_XBM=false;
        NETDEV_MODE=0
    fi

    if [[ ! -d /sys/class/net/${XPCI_NETDEV} ]]; then
        echo ">>> ERROR! No such interface: ${XPCI_NETDEV}"
        exit 1
    fi
    ATTACH_IF=${XPCI_NETDEV}
fi

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
insmod /home/admin/x1/xpci.ko attach_if=${ATTACH_IF} num_of_ports=${PORT_NUM} debug_level=${DEBUG_LEVEL} netdev_mode=${NETDEV_MODE}

echo ">>> Sleeping 5"
sleep 5

#echo ">>> Set XPCI debug level to INFO(3)"
#echo ${DEBUG_LEVEL} > /proc/sys/dev/xpci_dev/debug_level

if [[ ${USE_XBM} == "true" ]]; then
    echo ">>> Simulation mode. Use xbm!"
    touch /etc/sonic/use_xbm
    /home/admin/xbm/cfg/start.sh
fi

