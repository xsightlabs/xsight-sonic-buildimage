#!/bin/bash

set -x

num_ports=15
for i in `seq 0 ${num_ports}`
do
    ifconfig Ethernet${i} down
done

ifconfig Ethernet13 up
