#!/bin/bash

SYS_MODE="xbm"
XPCI_NETDEV_ATTACH_IF="xcpu"
# default netdev name for asic mode if config file doesn't exist or interface doesn't exist
DEFAULT_ASIC_NETDEV_NAME="xpcxd0"
SECOND_ASIC_NETDEV_NAME="eth10g0"
PORT_NUM=128
DEBUG_LEVEL=3
NETDEV_MODE=1
HW_IRQ_MODE=1
PCI_MODE=1
TX_CHECKSUMMING_MODE=0
DEFAULT_MTU=9200
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`
ONIE_PLATFORM=`sed -n -e 's/^.*onie_platform=//p' /host/machine.conf`
LABEL_REVISION_FILE="/etc/sonic/hw_revision"
XPLT_UTL="/opt/xplt/utils"

if [[ ${ONIE_MACHINE,,} == *"x2evb"* ]]; then
    if [[ "$(hostname)" == "sonic" ]]; then
        blk_dev="/dev/nvme0n1"
        part_name="Xsight-DIAG"

        part_num=`/usr/sbin/sgdisk -p $blk_dev | grep $part_name | xargs | cut -d' ' -f1`
        if [ -z "$part_num" ]; then
            echo "Error: Not found partition number for $part_name."
            exit 1
        fi

        mkdir -p /tmp/diag
        mount -t ext4 ${blk_dev}p${part_num} /tmp/diag
        evbhostname=$(cat /tmp/diag/etc/hostname)
        umount /tmp/diag
        rm -rf /tmp/diag

        sed -i "s/sonic/${evbhostname}/" /etc/sonic/config_db.json
        echo "{\"DEVICE_METADATA\": {\"localhost\" : {\"hostname\" : \"${evbhostname}\" }}}" > /tmp/hostname.json
        sonic-cfggen --write-to-db -j /tmp/hostname.json
        systemctl restart hostname-config.service
    fi
fi

if [[ ${ONIE_MACHINE,,} != *"kvm"* ]]; then
    # Probing cpu ixgbe net interfaces
    if [[ ! -d /sys/module/ixgbe ]]; then
        modprobe ixgbe
    fi

    SYS_MODE="asic"
    XPCI_NETDEV_ATTACH_IF=${DEFAULT_ASIC_NETDEV_NAME}

    if [[ ${SYS_MODE,,} != "xbm" && ! -d /sys/class/net/${XPCI_NETDEV_ATTACH_IF} ]]; then
        echo ">>> WARN! No such interface: ${XPCI_NETDEV_ATTACH_IF}, set to ${DEFAULT_ASIC_NETDEV_NAME}"
        XPCI_NETDEV_ATTACH_IF=${DEFAULT_ASIC_NETDEV_NAME}
    fi
fi

# Checking the label revision
if [ ${SYS_MODE,,} != "xbm" ]; then
    decode-syseeprom -d | grep "Label Revision" | awk '{print $5}' > ${LABEL_REVISION_FILE}
fi

if [[ ${XPCI_NETDEV_ATTACH_IF} == "xcpu" ]]; then
    echo ">>> Configuring CPU port VETH devices"
    # Setup CPU port
    ip link add name veth0 type veth peer name xcpu
    ip link set dev veth0 mtu ${DEFAULT_MTU} up
fi

ip link set dev ${XPCI_NETDEV_ATTACH_IF} mtu ${DEFAULT_MTU} up

if [[ ${SYS_MODE,,} == "xbm" ]]; then
    HW_IRQ_MODE=0
    PCI_MODE=0
fi
echo ">>> Re-load NetDev"

# Reset X1 and PCI bus
if [ -f /tmp/xbooted ]; then
    if [ ${SYS_MODE,,} != "xbm" ]; then
        if [ -d $XPLT_UTL ]; then
            echo ">>> Resetting X1"
            $XPLT_UTL/es9632x_reset_x1.sh
            if [ $? -ne 0 ]; then
                echo "ERROR: On running es9632x_reset_x1.sh"
            fi
        else
            echo "ERROR: No $XPLT_UTL found!"
        fi
    fi
fi

rmmod xpci
#read -p "--- Press enter to continue ---"
# TODO: change insmod to modprobe after moving xdrivers build into sonic-buildimage
# debug_level = 1 - Error
#               2 - Notice
#               3 - Info
#               4 - Debug
#               5 - Debug with Packet trace
modprobe xpci attach_if=${XPCI_NETDEV_ATTACH_IF} num_of_ports=${PORT_NUM} debug_level=${DEBUG_LEVEL} \
              netdev_mode=${NETDEV_MODE} hw_irq_mode=${HW_IRQ_MODE} pci_mode=${PCI_MODE} \
              tx_checksumming=${TX_CHECKSUMMING_MODE}

echo ">>> Sleeping 5"
sleep 5

if [ ! -f /tmp/xbooted ]; then
    if [ ${SYS_MODE,,} != "xbm" ]; then
        if [ -d $XPLT_UTL ]; then
            echo ">>> Configure xcvrs"
            cd $XPLT_UTL/xcvrs && /opt/xplt/venv/bin/python config.py -m 1
        else
            echo "ERROR: No $XPLT_UTL found!"
        fi
    fi
    /usr/local/bin/pip3 install /usr/share/sonic/device/$ONIE_PLATFORM/sonic_platform-1.0-py3-none-any.whl
    touch /tmp/xbooted
fi

#echo ">>> Set XPCI debug level to INFO(3)"
echo ${DEBUG_LEVEL} > /proc/sys/dev/xpci/debug_level

