ifneq ($(KERNELRELEASE),)
obj-m:= x86-64-es9632xq-cpld.o x86-64-es9632xq-sfp.o\
    x86-64-es9632xq-fan.o x86-64-es9632xq-leds.o \
    x86-64-es9632xq-psu.o x86-64-es9632xq-sys.o dps850.o

else
ifeq (,$(KERNEL_SRC))
$(error KERNEL_SRC is not defined)
else
KERNELDIR:=$(KERNEL_SRC)
endif
PWD:=$(shell pwd)
default:
	$(MAKE) -C $(KERNELDIR)  M=$(PWD) modules
clean:
	rm -rf *.o *.mod.o *.mod.o *.ko .*cmd .tmp_versions Module.markers Module.symvers modules.order
endif
