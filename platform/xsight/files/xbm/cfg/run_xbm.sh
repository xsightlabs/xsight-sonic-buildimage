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

declare -A port_mapping=( [eth1]=120 [eth2]=122 [eth3]=124 [eth4]=126 [eth5]=248 [eth6]=250
                          [eth7]=252 [eth8]=254 [eth9]=104 [eth10]=106 [eth11]=108 [eth12]=110
                          [eth13]=232 [eth14]=234 [eth15]=236 [eth16]=238 [eth17]=96 [eth18]=98
                          [eth19]=100 [eth20]=102 [eth21]=224 [eth22]=226 [eth23]=228 [eth24]=230
                          [eth25]=112 [eth26]=114 [eth27]=116 [eth28]=118 [eth29]=240 [eth30]=242
                          [eth31]=244 [eth32]=246 )

ports=$(ip -br link | grep -Po "eth[1-9].")
port_mapping_str=""
for port in $ports
do
    if [[ ${ONIE_MACHINE,,} != *"kvm"* ]]; then
        ip link add $port type dummy
    fi
    ip link set dev $port mtu ${DEFAULT_MTU} up
    port_mapping_str+=" -i ${port_mapping[$port]}@$port"
done
# CPU port
port_mapping_str+=" -i 256@veth0"
xbm_str+=" $port_mapping_str"
# start XBM
eval $xbm_str