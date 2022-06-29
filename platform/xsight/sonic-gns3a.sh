#!/bin/bash

# This script creates a .gns3a SONiC appliance file
IMGFILE="sonic-vs.image"
RELEASE="latest"

usage() {
    echo "`basename $0` [ -r <ReleaseNumber> ] -b <SONiC VS image: sonic-vs.image>"
    echo "e.g.: `basename $0` -r 1.1 -b <store_path>/sonic-vs.image"
    exit 0
}

while getopts "r:b:h" arg; do
  case $arg in
    h)
	usage
	;;
    r)
	RELEASE=$OPTARG
	;;
    b)
	IMGFILE=$OPTARG
	;;
  esac
done

if [ ! -e ${IMGFILE} ]; then
    echo "ERROR: ${IMGFILE} not found"
    exit 2
fi


MD5SUMIMGFILE=`md5sum  ${IMGFILE} | cut -f 1 -d " "`
LENIMGFILE=`stat -c %s ${IMGFILE}`
GNS3APPNAME="SONiC-${RELEASE}.gns3a"
NAMEIMGFILE=`basename $IMGFILE`

echo "
{
    \"name\": \"SONiC\",
    \"category\": \"router\",
    \"description\": \"SONiC Virtual Switch/Router\",
    \"vendor_name\": \"SONiC\",
    \"vendor_url\": \"https://azure.github.io/SONiC/\",
    \"product_name\": \"SONiC\",
    \"product_url\": \"https://azure.github.io/SONiC/\",
    \"registry_version\": 3,
    \"status\": \"experimental\",
    \"maintainer\": \"SONiC\",
    \"maintainer_email\": \"sonicproject@googlegroups.com\",
    \"usage\": \"Supports SONiC release: ${RELEASE}\",
    \"first_port_name\": \"eth0\",
    \"qemu\": {
        \"adapter_type\": \"e1000\",
        \"adapters\": 10,
        \"custom_adapters\": [
            {
                \"adapter_number\": 1,
                \"port_name\": \"Ethernet0\"
            },
            {
                \"adapter_number\": 2,
                \"port_name\": \"Ethernet8\"
            },
            {
                \"adapter_number\": 3,
                \"port_name\": \"Ethernet16\"
            },
            {
                \"adapter_number\": 4,
                \"port_name\": \"Ethernet24\"
            },
            {
                \"adapter_number\": 5,
                \"port_name\": \"Ethernet32\"
            },
            {
                \"adapter_number\": 6,
                \"port_name\": \"Ethernet40\"
            },
            {
                \"adapter_number\": 7,
                \"port_name\": \"Ethernet48\"
            },
            {
                \"adapter_number\": 8,
                \"port_name\": \"Ethernet56\"
            },
            {
                \"adapter_number\": 9,
                \"port_name\": \"Ethernet64\"
            }
        ],
        \"ram\": 2048,
        \"hda_disk_interface\": \"virtio\",
        \"arch\": \"x86_64\",
        \"console_type\": \"telnet\",
        \"boot_priority\": \"d\",
        \"kvm\": \"require\"
    },
    \"images\": [
        {
            \"filename\": \"${NAMEIMGFILE}\",
            \"version\": \"${RELEASE}\",
            \"md5sum\": \"${MD5SUMIMGFILE}\",
            \"filesize\": ${LENIMGFILE}
        }
    ],
    \"versions\": [
        {
            \"name\": \"${RELEASE}\",
            \"images\": {
                \"hda_disk_image\": \"${NAMEIMGFILE}\"
            }
        }
    ]
}

" > ${GNS3APPNAME}

