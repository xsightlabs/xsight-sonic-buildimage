# thrift package

THRIFT_0_22_0_VERSION = 0.22.0
THRIFT_0_22_0_VERSION_FULL = $(THRIFT_0_22_0_VERSION)

LIBTHRIFT_0_22_0 = libthrift0_$(THRIFT_0_22_0_VERSION)_$(CONFIGURED_ARCH).deb
$(LIBTHRIFT_0_22_0)_SRC_PATH = $(PLATFORM_PATH)/thrift
SONIC_MAKE_DEBS += $(LIBTHRIFT_0_22_0)

LIBTHRIFT_0_22_0_DEV = libthrift-dev_$(THRIFT_0_22_0_VERSION)_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBTHRIFT_0_22.0),$(LIBTHRIFT_0_22_0_DEV)))

PYTHON3_THRIFT_0_22.0 = python3-thrift_$(THRIFT_0_22_0_VERSION)_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBTHRIFT_0_22.0),$(PYTHON3_THRIFT_0_22.0)))

PYTHON_THRIFT_0_22.0 = python-thrift_$(THRIFT_0_22_0_VERSION)_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBTHRIFT_0_22.0),$(PYTHON_THRIFT_0_22.0)))

THRIFT_0_22_0_COMPILER = thrift-compiler_$(THRIFT_0_22_0_VERSION)_$(CONFIGURED_ARCH).deb
$(eval $(call add_derived_package,$(LIBTHRIFT_0_22.0),$(THRIFT_0_22_0_COMPILER)))
