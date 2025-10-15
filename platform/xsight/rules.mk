include $(PLATFORM_PATH)/xsight-sai.mk
include $(PLATFORM_PATH)/docker-syncd-xsight.mk
include $(PLATFORM_PATH)/docker-syncd-xsight-rpc.mk
include $(PLATFORM_PATH)/docker-saiserver-xsight.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/libsaithrift-dev.mk
#include $(PLATFORM_PATH)/docker-ptf-xsight.mk
include $(PLATFORM_PATH)/platform-modules-accton.mk
include $(PLATFORM_PATH)/platform-modules-xsight.mk
include $(PLATFORM_PATH)/xplt.mk
include $(PLATFORM_PATH)/onie.mk
include $(PLATFORM_PATH)/kvm-image.mk
include $(PLATFORM_PATH)/xpci.mk

SONIC_ALL += $(SONIC_ONE_IMAGE) \
             $(DOCKER_FPM) \
             $(DOCKER_SYNCD_XSIGHT)

# Inject SAI into sairedis
ifeq ($(ENABLE_SYNCD_RPC),y)
$(SYNCD)_DEPENDS += $(LIBSAITHRIFT_DEV)
endif

ifeq ($(LIBSAI_EXISTS),y)
$(SYNCD)_DEPENDS += $(XSIGHT_LIBSAI) $(XSIGHT_LIBSAI_DEV)
$(SYNCD)_UNINSTALLS += $(XSIGHT_LIBSAI_DEV)
else
$(SYNCD)_DEPENDS += $(XSIGHT_LIBSAI_GITHUB) $(XSIGHT_LIBSAI_DEV_GITHUB)
$(SYNCD)_UNINSTALLS += $(XSIGHT_LIBSAI_DEV_GITHUB)
endif

# Runtime dependency on xsight sai is set only for syncd
ifeq ($(LIBSAI_EXISTS),y)
$(SYNCD)_RDEPENDS += $(XSIGHT_LIBSAI)
else
$(SYNCD)_RDEPENDS += $(XSIGHT_LIBSAI_GITHUB)
endif
