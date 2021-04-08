#!/bin/bash

USE_XBM="/etc/sonic/use_xbm"

if [ -f "$USE_XBM" ]; then
    /home/admin/xbm/cfg/down.sh
fi

