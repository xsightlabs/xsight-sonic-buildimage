#!/bin/bash
#
# Usage: xcvr_setup.sh [init|deinit]
#

sysfs=/sys/bus/i2c/devices

i2c_config() {
    local count=0
    local MAX_BUS_RETRY=20
    local MAX_I2C_OP_RETRY=10

    i2c_bus_op=`echo "$@" | cut -d'>' -f 2`
    i2c_bus=$(dirname $i2c_bus_op)

    # check if bus exists
    while [[ "$count" -lt "$MAX_BUS_RETRY" ]]; do
        [[ -e $i2c_bus ]] && break || sleep .1
        count=$((count+1))
    done

    if [[ "$count" -eq "$MAX_BUS_RETRY" ]]; then
        echo "ERROR: $@ : i2c bus not created"
        return
    fi

    # perform the add/delete
    count=0
    while [[ "$count" -lt "$MAX_I2C_OP_RETRY" ]]; do
        eval "$@" > /dev/null 2>&1
        [[ $? == 0 ]] && break || sleep .2
        count=$((count+1))
    done

    if [[ "$count" -eq "$MAX_I2C_OP_RETRY" ]]; then
        echo "ERROR: $@ : i2c operation failed"
        return
    fi
}

init_devnum() {
    found=0
    for devnum in 0 1 2; do
        devname=`cat $sysfs/i2c-$devnum/name`
        if [[ $devname == 'FT260 usb-i2c bridge'* ]]; then
            found=1
            break
        fi
    done

    [[ $found -eq 0 ]] && echo "cannot find FT260" && exit 1
}

stage_1() {
    case $1 in
        "new_device")
                       i2c_config "echo pca9548 0x72 > $sysfs/i2c-$devnum/$1"
                       i2c_config "echo pca9548 0x73 > $sysfs/i2c-$devnum/$1"
                       i2c_config "echo 24c02 0x57 > $sysfs/i2c-$devnum/$1"
                       sleep 1
                       echo -2 > $sysfs/i2c-$devnum/$devnum-0072/idle_state
                       echo -2 > $sysfs/i2c-$devnum/$devnum-0073/idle_state
                       ;;
        "delete_device")
                       i2c_config "echo 0x73 > $sysfs/i2c-$devnum/$1"
                       i2c_config "echo 0x72 > $sysfs/i2c-$devnum/$1"
                       i2c_config "echo 0x57 > $sysfs/i2c-$devnum/$1"
                       ;;
        *)             echo "stage_1: invalid command!"
                       ;;
    esac
}

#Attach/Detach optoe3 on 0x50
stage_2() {
    local idx_bgn=$(expr $devnum + 1)
    local idx_end=$(expr $idx_bgn + $PORTS)
    case $1 in
        "new_device")
                      for (( i=$idx_bgn; i<$idx_end; i++ ))
                      do
                          mux_idx=$(expr $i - $idx_bgn)
                          mux_idx=$(expr 1  + $mux_idx)
                          #echo "Attaching optoe3 $mux_idx to i2c-$i"
                          i2c_config "echo optoe3 0x50 > $sysfs/i2c-$i/$1"
                          echo "port$mux_idx" > "$sysfs/$i-0050/port_name"
                      done
                      ;;
        "delete_device")
                      for (( i=$idx_bgn; i<$idx_end; i++ ))
                      do
                          mux_idx=$(expr $i - $idx_bgn)
                          mux_idx=$(expr 1  + $mux_idx)
                          #echo "Detaching optoe3 $mux_idx from i2c-$i"
                          i2c_config "echo 0x50 > $sysfs/i2c-$i/$1"
                      done
                      ;;
        *)            echo "fp_optoe: invalid command!"
                      ;;
    esac
}

MOD_DIR=../../modules
PORTS=16
E_BADARGS=85

if [ ! -n "$1" ];
then
    echo "Usage: $0 [init|deinit]"
    exit $E_BADARGS
fi
if [[ "$1" == "init" ]]; then
    lsmod | grep -q ft260 && rmmod hid_ft260
    lsmod | grep -q optoe && rmmod optoe
    depmod -a
    modprobe hid-ft260
    modprobe optoe
    init_devnum
    stage_1 "new_device"
    stage_2 "new_device"
elif [[ "$1" == "deinit" ]]; then
    init_devnum
    stage_2 "delete_device"
    stage_1 "delete_device"
    modprobe -rq hid-ft260
    modprobe -rq optoe
fi
