include $(PLATFORM_PATH)/xsight-sai.mk
include $(PLATFORM_PATH)/docker-syncd-xsight.mk
include $(PLATFORM_PATH)/docker-orchagent-xsight.mk
#include $(PLATFORM_PATH)/docker-syncd-xsight-rpc.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/libsaithrift-dev.mk
#include $(PLATFORM_PATH)/docker-ptf-xsight.mk

SONIC_ALL += $(SONIC_ONE_IMAGE) \
             $(DOCKER_FPM) \
             $(DOCKER_SYNCD_XSIGHT)

# Inject SAI into sairedis
$(LIBSAIREDIS)_DEPENDS += $(XSIGHT_SAI) $(XSIGHT_LIBSAI)
ifeq ($(ENABLE_SYNCD_RPC),y)
$(LIBSAIREDIS)_DEPENDS += $(LIBSAITHRIFT_DEV)
endif

# Runtime dependency on xsight sai is set only for syncd
$(SYNCD)_RDEPENDS += $(XSIGHT_LIBSAI)
