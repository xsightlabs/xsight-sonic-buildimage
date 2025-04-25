.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

XPCI_NAME =  xpci-dkms_$(XPCI_VERSION)_amd64
#SRC_DEB = $(XPCI_NAME).deb
MOD_DEB_NAME = xpci-modules-$(KVERSION)
MOD_DEB = $(MOD_DEB_NAME)_$(XPCI_VERSION)_amd64.deb

MAIN_TARGET = $(MOD_DEB)

DKMS_BMDEB = /var/lib/dkms/xpci/$(XPCI_VERSION)/bmdeb
DKMS_TMP := $(shell mktemp -u -d -t dkms.XXXXXXXXXX)

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
#	rm -rf $(SRC_DEB)
#	wget --password swswsw sw@xftp.xsightlabs.com:/$(SRC_DEB)

	# put a lock here because dpkg does not allow installing packages in parallel
#	while true; do
#	if mkdir $(DEST)/dpkg_lock &> /dev/null; then
#	{ sudo dpkg -i $(DEST)/$(SRC_DEB) && rm -d $(DEST)/dpkg_lock && break; } || { rm -d $(DEST)/dpkg_lock && exit 1 ; }
#	fi
#	done

	mkdir -p $(DKMS_TMP)/DEBIAN

	mkdir -p $(DKMS_TMP)/lib/modules/$(KVERSION)/updates/dkms

	cp /lib/modules/$(KVERSION)/updates/dkms/xpci.ko $(DKMS_TMP)/lib/modules/$(KVERSION)/updates/dkms

	# Create the control file for the package
	echo -e "Package: $(MOD_DEB_NAME)\n\
	Version: $(XPCI_VERSION) \n\
	Architecture: amd64 \n\
	Maintainer: Kirill Tsym <kirillt@xsightlabs.com> \n\
	Description: XPCI kernel module for SONiC project" \
	> $(DKMS_TMP)/DEBIAN/control

	echo "12" > $(DKMS_TMP)/DEBIAN/compat

	echo "echo 'blacklist xpci' >> /etc/modprobe.d/xpci.conf" >> $(DKMS_TMP)/DEBIAN/postinst

	chmod 755 $(DKMS_TMP)/DEBIAN/postinst

	mkdir -p $(XPCI_NAME)/DEBS
	pushd $(XPCI_NAME)/DEBS
	dpkg -b $(DKMS_TMP) .
	popd

	rm -rf $(DKMS_TMP)

	cp $(XPCI_NAME)/DEBS/*.deb $(DEST)
