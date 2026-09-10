SHELL = /bin/bash
.ONESHELL:
.SHELLFLAGS += -e

MAIN_TARGET = libprotobuf32_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb
DERIVED_TARGETS = protobuf-compiler_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					libprotobuf-dev_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					libprotobuf-lite32_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					libprotoc32_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb \
					python3-protobuf_$(PROTOBUF_VERSION_FULL)_$(CONFIGURED_ARCH).deb

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	# Remove any stale files
	rm -rf protobuf-$(PROTOBUF_VERSION)

	# 3.21.12-3 is bookworm; live debian pool only has 3.21.12-11+deb13u1 now.
	# archive.debian.org does not have it (never a bullseye package).
	dget -u protobuf_$(PROTOBUF_VERSION_FULL).dsc http://snapshot.debian.org/archive/debian/20260201T000000Z/pool/main/p/protobuf/protobuf_$(PROTOBUF_VERSION_FULL).dsc

	pushd protobuf-$(PROTOBUF_VERSION)

ifeq ($(CROSS_BUILD_ENVIRON), y)
	dpkg-buildpackage -us -uc -b -a$(CONFIGURED_ARCH) -Pcross,nocheck -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
else
	dpkg-buildpackage -us -uc -b -j$(SONIC_CONFIG_MAKE_JOBS) --admindir $(SONIC_DPKG_ADMINDIR)
endif

	popd

	mv $(DERIVED_TARGETS) $* $(DEST)/

$(addprefix $(DEST)/, $(DERIVED_TARGETS)): $(DEST)/% : $(DEST)/$(MAIN_TARGET)
