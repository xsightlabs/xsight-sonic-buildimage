#!/bin/bash

SYS_MODE="xbm"
XPCI_NETDEV_ATTACH_IF="xcpu"
# default netdev name for asic mode if config file doesn't exist or interface doesn't exist
DEFAULT_ASIC_NETDEV_NAME="eth10g1"
SECOND_ASIC_NETDEV_NAME="eth10g0"
PORT_NUM=256
DEBUG_LEVEL=3
NETDEV_MODE=1
HW_IRQ_MODE=1
PCI_MODE=1
TX_CHECKSUMMING_MODE=0
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`
CFG_FILE="/etc/sonic/xlink.cfg"

if [[ ${ONIE_MACHINE,,} != *"kvm"* ]]; then
    # Working on HW box. Determine what to run XBM/ASIC
    if [[ -f ${CFG_FILE} ]]; then
        SYS_MODE=`sed -n -e 's/^.*sys_mode[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
        XPCI_NETDEV_ATTACH_IF=`sed -n -e 's/^.*xpci_netdev[[:blank:]]*=[[:blank:]]*//p' ${CFG_FILE}`
    else
        echo ">>> WARN! Config file not found: ${CFG_FILE}"
        SYS_MODE="asic"
        XPCI_NETDEV_ATTACH_IF=${DEFAULT_ASIC_NETDEV_NAME}
    fi

    # Probe patched ixgbe module if required
    if [[ ! -d /sys/class/xpci/xpci ]]; then
        ip link set dev ${SECOND_ASIC_NETDEV_NAME} down
        ip link set dev ${DEFAULT_ASIC_NETDEV_NAME} down
        sleep 1
        ip link set dev ${DEFAULT_ASIC_NETDEV_NAME} up

        ip link set dev ${DEFAULT_ASIC_NETDEV_NAME} down
        ip link set dev ${DEFAULT_ASIC_NETDEV_NAME} up

    else
        ip link set dev ${SECOND_ASIC_NETDEV_NAME} down
        ip link set dev ${DEFAULT_ASIC_NETDEV_NAME} down
        sleep 1
        ip link set dev ${DEFAULT_ASIC_NETDEV_NAME} up
    fi

    if [[ ${SYS_MODE,,} != "xbm" && ! -d /sys/class/net/${XPCI_NETDEV_ATTACH_IF} ]]; then
        echo ">>> WARN! No such interface: ${XPCI_NETDEV_ATTACH_IF}, set to ${DEFAULT_ASIC_NETDEV_NAME}"
        XPCI_NETDEV_ATTACH_IF=${DEFAULT_ASIC_NETDEV_NAME}
    fi
fi

if [[ ${XPCI_NETDEV_ATTACH_IF} == "xcpu" ]]; then
    echo ">>> Configuring CPU port VETH devices"
    # Setup CPU port
    ip link add name veth0 type veth peer name xcpu
    ip link set dev veth0 up
    ip link set dev xcpu up
fi

if [[ ${SYS_MODE,,} == "xbm" ]]; then
    HW_IRQ_MODE=0
    PCI_MODE=0
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
insmod /home/admin/xlx/xpci.ko attach_if=${XPCI_NETDEV_ATTACH_IF} num_of_ports=${PORT_NUM} debug_level=${DEBUG_LEVEL} \
                               netdev_mode=${NETDEV_MODE} hw_irq_mode=${HW_IRQ_MODE} pci_mode=${PCI_MODE} \
                               tx_checksumming=${TX_CHECKSUMMING_MODE}

echo ">>> Sleeping 5"
sleep 5

#echo ">>> Set XPCI debug level to INFO(3)"
#echo ${DEBUG_LEVEL} > /proc/sys/dev/xpci_dev/debug_level

if [[ ${SYS_MODE,,} == "xbm" ]]; then
    echo ">>> Simulation mode. Use xbm!"
    /home/admin/xbm/cfg/start.sh
fi
