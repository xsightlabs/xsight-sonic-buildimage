# Xsight xpci

XPCI_VERSION = 1.0

export XPCI_VERSION

XSIGHT_XPCI_URL_PREFIX = "file:///sonic"
XPCI = xpci-dkms_$(XPCI_VERSION)_amd64.deb
$(XPCI)_URL = "$(XSIGHT_XPCI_URL_PREFIX)/$(XPCI)"

XPCI_EXISTS := $(or $(and $(wildcard $(XPCI)),y),n)

ifeq ($(XPCI_EXISTS),y)
SONIC_ONLINE_DEBS += $(XPCI)
endif

KERNEL_XPCI = xpci-modules-$(KVERSION)_$(XPCI_VERSION)_amd64.deb
ifeq ($(XPCI_EXISTS),y)
$(KERNEL_XPCI)_DEPENDS += $(LINUX_HEADERS) $(LINUX_HEADERS_COMMON) $(XPCI)

$(KERNEL_XPCI)_SRC_PATH = $(PLATFORM_PATH)/xpci
SONIC_MAKE_DEBS += $(KERNEL_XPCI)
else
$(KERNEL_XPCI)_URL = "https://github.com/xsightlabs/sonic-xsight-binaries/raw/refs/heads/main/amd64/kernel/$(KERNEL_XPCI)"
SONIC_ONLINE_DEBS += $(KERNEL_XPCI)
endif
