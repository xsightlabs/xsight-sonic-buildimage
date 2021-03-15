#!/bin/bash

#set -x

export XSAI_CFG=${PWD}"/xlink_cfg.json"

# Full API debug
#export XLOG_DEBUG="SWL SWL-SAI XAPI SAI XSAI XHAL-LIB XHAL-TBL XHAL-LPM XDRV-MBR XBM-DRV-API XDRV-COMMON XPCI-DRV"
#export XLOG_DEBUG="SWL SAI XAPI XHAL XDRV XBM XPCI"
export XLOG_DEBUG="ALL"
export XLOG_LEVEL=DEBUG
export SAI_RPC_PORT="50000"
export XSAI_RPC_PORT="50001"
export XHAL_RPC_PORT="50002"
export XLOG_FILE=${PWD}"/../log/xlink.log"

echo "----------------------------------------"
echo "BASE_DIR      : " ${BASE_DIR}
echo "XSAI_CFG      : " ${XSAI_CFG}
echo "XLOG_DEBUG    : " ${XLOG_DEBUG}
echo "XLOG_LEVEL    : " ${XLOG_LEVEL}
echo "XLOG_FILE     : " ${XLOG_FILE}
echo "SAI_RPC_PORT  : " ${SAI_RPC_PORT}
echo "XSAI_RPC_PORT : " ${XSAI_RPC_PORT}
echo "XHAL_RPC_PORT : " ${XHAL_RPC_PORT}
echo "----------------------------------------"
