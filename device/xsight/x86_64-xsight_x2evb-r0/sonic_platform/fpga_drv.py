# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 Xsightlabs Ltd.

from ctypes import *

# Define configuration parameters of libfpga_drv.so for both I2C + SPI interfaces.
# interface: 0-N/A, 1-I2C, 2-SPI
interface = 1
# Define input variables for I2C interface
bus_id = 1
i2c_slv = 0x18
# Define input variables for SPI interface
ft_ch_num = 1

# Define FPGA registers
reg_osfp_interrupt_sts = 0x330
reg_osfp_present_sts = 0x338
reg_osfp_low_power = 0x340
reg_osfp_reset = 0x348

lib = CDLL('/opt/xplt/utils/fpga/fpga_drv/libfpga_drv.so')

class i2c_parameters(Structure):
	_fields_ = [("bus_id", c_int)]

class spi_parameters(Structure):
	_fields_ = [("ft_ch_num", c_int)]

class fpga_parameters(Structure):
	_fields_ = [("i2cdrv_params", i2c_parameters),
			("spidrv_params", spi_parameters),
			("interface", c_int),
			("i2c_slv", c_ubyte)]

fpga_init = lib.fpga_init
fpga_init.argtypes = [POINTER(fpga_parameters)]
fpga_init.restype = c_int

fpga_free = lib.fpga_free
fpga_free.argtypes = []
fpga_free.restype = c_int

fpga_reg_read = lib.fpga_reg_read
fpga_reg_read.argtypes = [c_int, POINTER(c_longlong)]
fpga_reg_read.restype = c_int

fpga_reg_read_modify_write = lib.fpga_reg_read_modify_write
fpga_reg_read_modify_write.argtypes = [c_int, c_longlong, c_longlong]
fpga_reg_read_modify_write.restype = c_int

c_i2c = i2c_parameters(bus_id)
c_spi = spi_parameters(ft_ch_num)
c_fpga = fpga_parameters(c_i2c, c_spi, interface, i2c_slv)

def read_fpga_reg(reg):
	"""Read FPGA register via libfpga_drv.so using Python's ctype module.

	Args:
		reg: integer of FPGA register address.

	Returns:
		Integer of FPGA register value.
	"""
	val = c_longlong()
	fpga_init(byref(c_fpga))
	fpga_reg_read(reg, byref(val))
	fpga_free()
	return int(val.value)

def read_modify_write_fpga_reg(reg, mask, val):
	"""Write FPGA register via libfpga_drv.so using Python's ctype module.

	Args:
		reg: integer of FPGA register address.
		mask: integer of FPGA register mask value.
		val: integer of value to be write to FPGA register.

	Returns:
		None.
	"""
	fpga_init(byref(c_fpga))
	fpga_reg_read_modify_write(reg, mask, val)
	fpga_free()
