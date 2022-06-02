.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

XPCI_NAME =  xpci-dkms_$(XPCI_VERSION)_amd64
#SRC_DEB = $(XPCI_NAME).deb
MOD_DEB = xpci-modules-$(KVERSION)_$(XPCI_VERSION)_amd64.deb

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

	sudo dkms build xpci/$(XPCI_VERSION) -k $(KVERSION) -a amd64
	sudo dkms mkbmdeb xpci/$(XPCI_VERSION) -k $(KVERSION) -a amd64

	# w/a: remove dependencies
	mkdir -p $(DKMS_TMP)/DEBIAN

	dpkg -e $(DKMS_BMDEB)/$(MOD_DEB) $(DKMS_TMP)/DEBIAN
	dpkg -x $(DKMS_BMDEB)/$(MOD_DEB) $(DKMS_TMP)

	sed -i '/^Depends:/c\Depends:' $(DKMS_TMP)/DEBIAN/control

	mkdir -p $(XPCI_NAME)/DEBS
	pushd $(XPCI_NAME)/DEBS
	dpkg -b $(DKMS_TMP) .
	popd

	rm -rf $(DKMS_TMP)

	cp $(XPCI_NAME)/DEBS/*.deb $(DEST)
