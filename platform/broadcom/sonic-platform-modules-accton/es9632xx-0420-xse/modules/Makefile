ifneq ($(KERNELRELEASE),)
obj-m:= x86-64-es9632xx-0420-xse-cpld.o x86-64-es9632xx-0420-xse-sfp.o\
    x86-64-es9632xx-0420-xse-fan.o x86-64-es9632xx-0420-xse-leds.o \
    x86-64-es9632xx-0420-xse-psu.o x86-64-es9632xx-0420-xse-sys.o dps850.o

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
