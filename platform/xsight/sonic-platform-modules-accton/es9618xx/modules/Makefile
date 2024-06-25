obj-m += optoe.o
obj-m += x86-64-es9618xx-cpld.o \
	x86-64-es9618xx-fan.o x86-64-es9618xx-leds.o \
	x86-64-es9618xx-psu.o dps850.o

# Uncomment to enable debug tracing in the driver.
#CFLAGS_optoe.o := -DDEBUG

all:
	sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	sudo make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
