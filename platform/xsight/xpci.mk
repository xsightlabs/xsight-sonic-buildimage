# Xsight xpci

XPCI_VERSION = 1.0

export XPCI_VERSION

XSIGHT_URL = file:///sonic
XPCI = xpci-dkms_$(XPCI_VERSION)_amd64.deb
$(XPCI)_URL = $(XSIGHT_URL)/$(XPCI)
SONIC_ONLINE_DEBS += $(XPCI)

$(eval $(call add_derived_package,$(XPCI)))

KERNEL_XPCI = xpci-modules-$(KVERSION)_$(XPCI_VERSION)_amd64.deb
$(KERNEL_XPCI)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON) $(XPCI)

$(KERNEL_XPCI)_SRC_PATH = $(PLATFORM_PATH)/xpci
SONIC_MAKE_DEBS += $(KERNEL_XPCI)

$(eval $(call add_derived_package,$(KERNEL_XPCI)))

