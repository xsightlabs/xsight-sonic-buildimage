.ONESHELL:
SHELL = /bin/bash
.SHELLFLAGS += -e

MAIN_TARGET = ixgbe.ko

$(addprefix $(DEST)/, $(MAIN_TARGET)): $(DEST)/% :
	rm -rf ./ixgbe
	git clone ssh://git@x-git01.xsight.ent:7999/xs/ixgbe.git
	pushd ./ixgbe
	# Build the package
	pushd src
	export BUILD_KERNEL=$(KVERSION)
	make
	popd
	popd
	mv ./ixgbe/src/$* $(DEST)/
