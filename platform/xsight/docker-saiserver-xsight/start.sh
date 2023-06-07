#!/usr/bin/env bash

LABEL_REVISION_FILE="/etc/sonic/hw_revision"

ln -sf /usr/share/sonic/hwsku/xdrv_config.json /etc/xsight/xdrv_config.json
ln -sf /usr/share/sonic/hwsku/xlink_cfg.json /etc/xsight/xlink_cfg.json
ln -sf /usr/share/sonic/hwsku/lanes_polarity.json /etc/xsight/lanes_polarity.json
/usr/bin/init_xsai.sh

if [ -f  ${LABEL_REVISION_FILE} ]; then
    LABEL_REVISION=`cat ${LABEL_REVISION_FILE}`
    if [[ x${LABEL_REVISION} == x"R0B" ]] || [[ x${LABEL_REVISION} == x"R0B2" ]]; then
        ln -sf /etc/xsight/serdes_config_A0.json /etc/xsight/serdes_config.json
    else
        ln -sf /etc/xsight/serdes_config_A1.json /etc/xsight/serdes_config.json
    fi
fi

rm -f /var/run/rsyslogd.pid

supervisorctl start rsyslogd

supervisorctl start saiserver
