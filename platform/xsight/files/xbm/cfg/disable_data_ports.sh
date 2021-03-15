#!/bin/bash

set -x

num_ports=16
for i in `seq 1 ${num_ports}`
do
    ifconfig eth${i} down
done

ifconfig eth14 up
