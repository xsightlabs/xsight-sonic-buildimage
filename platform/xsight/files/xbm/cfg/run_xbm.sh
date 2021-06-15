#!/bin/bash
ONIE_MACHINE=`sed -n -e 's/^.*onie_machine=//p' /host/machine.conf`

set -x

echo ">>> Looking for running XBM process"

if pgrep -x "xbm" >/dev/null
then
    echo "XBM is running. Stopping it..."
    kill -9 `pidof xbm`
    sleep 1
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
    ifconfig eth${i} up
done

/home/admin/xbm/bin/xbm --device-id 0 --name standalone0 --thrift-port 49153 \
	--log-file /home/admin/xbm/log/standalone0_log_file.log --pcap -L error --log-flush --enforce-validation \
	--dpu-x-size 4 --dpu-y-size 4 --ifu-config-mode 0 \
	-i 0@eth1 -i 1@eth2 -i 2@eth3 -i 3@eth4 -i 4@eth5 -i 5@eth6 -i 6@eth7 \
	-i 7@eth8 -i 64@eth9 -i 65@eth10 -i 66@eth11 -i 67@eth12 -i 68@eth13 -i 69@eth14 -i 70@eth15 -i 71@eth16 \
	-i 256@veth0
