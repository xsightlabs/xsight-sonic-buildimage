.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

MAIN_TARGET = ixgbe.ko

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	pushd ./ixgbe
	# Build the package
	pushd src
	export BUILD_KERNEL=$(KVERSION)
	make
	popd
	popd
	mv ./ixgbe/src/$* $(DEST)/
