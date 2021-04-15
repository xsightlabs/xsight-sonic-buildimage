include $(PLATFORM_PATH)/xsight-sai.mk
include $(PLATFORM_PATH)/docker-syncd-xsight.mk
#include $(PLATFORM_PATH)/docker-syncd-xsight-rpc.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/libsaithrift-dev.mk
#include $(PLATFORM_PATH)/docker-ptf-xsight.mk
include $(PLATFORM_PATH)/platform-modules-accton.mk

SONIC_ALL += $(SONIC_ONE_IMAGE) \
             $(DOCKER_FPM) \
             $(DOCKER_SYNCD_XSIGHT)

# Inject SAI into sairedis
ifeq ($(ENABLE_SYNCD_RPC),y)
$(SYNCD)_DEPENDS += $(LIBSAITHRIFT_DEV)
endif

$(SYNCD)_DEPENDS += $(XSIGHT_LIBSAI) $(XSIGHT_LIBSAI_DEV)
$(SYNCD)_UNINSTALLS += $(XSIGHT_LIBSAI_DEV)


# Runtime dependency on xsight sai is set only for syncd
$(SYNCD)_RDEPENDS += $(XSIGHT_LIBSAI)
