#!/bin/bash

USE_XBM=true
ATTACH_IF="xcpu"
PORT_NUM=32
DEBUG_LEVEL=3
NETDEV_MODE=1
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`
CFG_FILE="/etc/sonic/xlink.cfg"

function get_hw_params {
    if [[ ! -f ${CFG_FILE} ]]; then
        echo ">>> WARN! Config file not found: ${CFG_FILE}"
        SYS_MODE="asic"
        XPCI_NETDEV="eth1"
    fi

    SYS_MODE=`sed -n -e 's/^.*sys_mode[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
    XPCI_NETDEV=`sed -n -e 's/^.*xpci_netdev[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
}

if [[ ${ONIE_MACHINE,,} == *"kvm"* ]]; then
    echo ">>> Configuring CPU port VETH devices"
    # Setup CPU port
    ip link add name veth0 type veth peer name xcpu
    ip link set dev veth0 up
    ip link set dev xcpu up
else
    # Working on HW box. Determine what to run XBM/ASIC
    get_hw_params
    if [[ ${SYS_MODE,,} != "xbm" ]]; then
        USE_XBM=false;
    fi

    if [[ ! -d /sys/class/net/${XPCI_NETDEV} ]]; then
        echo ">>> WARN! No such interface: ${XPCI_NETDEV}, set to eth1"
        XPCI_NETDEV="eth1"
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
    /home/admin/xbm/cfg/start.sh
fi

