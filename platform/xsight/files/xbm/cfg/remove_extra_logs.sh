#!/bin/bash

#leave logs with two digits numbering at max
while true
do
  sudo rm -f /home/admin/xbm/log/*.log.???.txt
  sleep 10
done
