#!/bin/bash
DEFAULT_MTU=9200
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`

set -x

echo ">>> Looking for running XBM process"

if pgrep -x "xbm" >/dev/null
then
    echo "XBM is running. Stopping it..."
    pkill -x -9 xbm
else
    echo "XBM is not running"
fi

echo ">>> Starting XBM process"
export LD_LIBRARY_PATH=/home/admin/xbm/bin

num_ports=32
for i in `seq 1 ${num_ports}`
do
    if [[ ${ONIE_MACHINE,,} != *"kvm"* ]]; then
        ip link add eth${i} type dummy
    fi
    ip link set dev eth${i} mtu ${DEFAULT_MTU} up
done

/home/admin/xbm/bin/xbm --device-id 0 --name standalone0 --thrift-port 49153 \
        --log-file /home/admin/xbm/log/standalone0_log_file.log -L off --log-flush \
        --enforce-validation --dpu-x-size 16 --dpu-y-size 16 --ifu-config-mode 0 \
        -i 120@eth1 -i 122@eth2 -i 124@eth3 -i 126@eth4 -i 248@eth5 -i 250@eth6 -i 252@eth7 -i 254@eth8 \
        -i 104@eth9 -i 106@eth10 -i 108@eth11 -i 110@eth12 -i 232@eth13 -i 234@eth14 -i 236@eth15 -i 238@eth16 \
        -i 96@eth17 -i 98@eth18 -i 100@eth19 -i 102@eth20 -i 224@eth21 -i 226@eth22 -i 228@eth23 -i 230@eth24 \
        -i 112@eth25 -i 114@eth26 -i 116@eth27 -i 118@eth28 -i 240@eth29 -i 242@eth30 -i 244@eth31 -i 246@eth32 \
        -i 256@veth0
