#!/bin/bash

SYS_MODE="xbm"
XPCI_NETDEV="xcpu"
# default netdev name for asic mode if config file doesn't exist or interface doesn't exist
DEFAULT_ASIC_NETDEV_NAME="eth1"
PORT_NUM=32
DEBUG_LEVEL=3
NETDEV_MODE=1
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`
CFG_FILE="/etc/sonic/xlink.cfg"

if [[ ${ONIE_MACHINE,,} != *"kvm"* ]]; then
    # Working on HW box. Determine what to run XBM/ASIC
    if [[ -f ${CFG_FILE} ]]; then
        SYS_MODE=`sed -n -e 's/^.*sys_mode[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
        XPCI_NETDEV=`sed -n -e 's/^.*xpci_netdev[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
    else
        echo ">>> WARN! Config file not found: ${CFG_FILE}"
        SYS_MODE="asic"
        XPCI_NETDEV=${DEFAULT_ASIC_NETDEV_NAME}
    fi

    if [[ ${SYS_MODE,,} != "xbm" && ! -d /sys/class/net/${XPCI_NETDEV} ]]; then
        echo ">>> WARN! No such interface: ${XPCI_NETDEV}, set to ${DEFAULT_ASIC_NETDEV_NAME}"
        XPCI_NETDEV=${DEFAULT_ASIC_NETDEV_NAME}
    fi
fi

if [[ ${XPCI_NETDEV} == "xcpu" ]]; then
    echo ">>> Configuring CPU port VETH devices"
    # Setup CPU port
    ip link add name veth0 type veth peer name xcpu
    ip link set dev veth0 up
    ip link set dev xcpu up
fi

echo ">>> Re-load NetDev"
#read -p "--- Press enter to continue ---"
rmmod xpci
# TODO: change insmod to modprobe after moving xdrivers build into sonic-buildimage
# debug_level = 1 - Error
#               2 - Notice
#               3 - Info
#               4 - Debug
#               5 - Debug with Packet trace
insmod /home/admin/x1/xpci.ko attach_if=${XPCI_NETDEV} num_of_ports=${PORT_NUM} debug_level=${DEBUG_LEVEL} netdev_mode=${NETDEV_MODE}

echo ">>> Sleeping 5"
sleep 5

#echo ">>> Set XPCI debug level to INFO(3)"
#echo ${DEBUG_LEVEL} > /proc/sys/dev/xpci_dev/debug_level

if [[ ${SYS_MODE,,} == "xbm" ]]; then
    echo ">>> Simulation mode. Use xbm!"
    /home/admin/xbm/cfg/start.sh
fi

