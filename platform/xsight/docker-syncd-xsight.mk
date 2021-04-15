# docker image for XSight Labs syncd

DOCKER_SYNCD_PLATFORM_CODE = xsight
include $(PLATFORM_PATH)/../template/docker-syncd-base.mk

$(DOCKER_SYNCD_BASE)_DEPENDS += $(SYNCD) $(LIBTHRIFT)

$(DOCKER_SYNCD_BASE)_RUN_OPT += --env ASAN_SAI_PLUGIN=${ASAN_SAI_PLUGIN} # used in address-sanitizer sai-plugin check

