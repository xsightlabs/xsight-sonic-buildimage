echo ">>> Init interfaces"
num_ports=3
for i in `seq 0 ${num_ports}`
do
    port_id=$((i + 1))
    echo ">>> Port ID: ["$port_id"] Interface: ["Ethernet${i}"]"
    ./xrtnlcfg --if-name Ethernet${i} --add --port $port_id
    ./setup_host.sh Ethernet${i}
    read -p "--- Press enter to continue ---"
done

