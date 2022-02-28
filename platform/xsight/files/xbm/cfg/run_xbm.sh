#!/bin/bash
DEFAULT_MTU=9200
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`

set -x

echo ">>> Looking for running XBM process"

if pgrep -x "xbm" >/dev/null
then
    echo "XBM is running. Stopping it..."
    pkill -x xbm
else
    echo "XBM is not running"
fi

echo ">>> Starting XBM process"
export LD_LIBRARY_PATH=/home/admin/xbm/bin
xbm_str="/home/admin/xbm/bin/xbm --device-id 0 --name standalone0 --thrift-port 49153 \
         --log-file /home/admin/xbm/log/standalone0_log_file.log -L off --log-flush \
         --enforce-validation --dpu-x-size 16 --dpu-y-size 16 --ifu-config-mode 0"
ports=$(ip -br link | grep -Po "eth[1-9].")
xbm_ports_mapping=""
map_id=0
step=2
for port in $ports
do
    if [[ ${ONIE_MACHINE,,} != *"kvm"* ]]; then
        ip link add $port type dummy
    fi
    ip link set dev $port mtu ${DEFAULT_MTU} up
    xbm_ports_mapping+=" -i $map_id@$port"
    let map_id=$map_id+$step
done
# CPU port
xbm_ports_mapping+=" -i 256@veth0"
xbm_str+=" $xbm_ports_mapping"
# start XBM
eval $xbm_str
