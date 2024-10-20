# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 Xsightlabs Ltd.

try:
    from sonic_platform.fpga_drv import *
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class XcvrPins:
	"""
	A class used to set/get xcvr discrete signal state.

	Attributes:
		ports_num: integer indicates number of ports.
	"""

	def __init__(self, ports_num):
		self.fpgadrv = FpgaDrv()
		self.ports_num = ports_num
		self.ports_mask = 0
		for port in range(0, ports_num):
			self.ports_mask |= (1 << port)

	def __get_xcvr_pin_state(self, reg):
		"""Get xcvr pin state for input `reg` for all ports.

		Args:
			reg: integer of FPGA register address.

		Returns:
			Integer representing bitmap of pin state for each port
			number or None in case of error.

		Notes:
			The returned pin state value depands on the specific pin.
			The pins description can be found at:
			http://soc.xsight.ent/app/index.cgi?
		"""
		return self.fpgadrv.read_fpga_reg(reg)

	def __set_xcvr_pin_state(self, reg, port_bitmap, state):
		"""Set xcvr pin state for input `reg` for all ports.

		Args:
			reg: integer of FPGA register address.
			port_bitmap: integer representing bitmap of port numbers.
			state: integer representing the pin state to change for.

		Returns:
			None.

		Notes:
			The input pin state value depands on the specific pin.
			The pins description can be found at:
			http://soc.xsight.ent/app/index.cgi?
		"""
		val = 0
		if state == 1:
			val = port_bitmap
		self.fpgadrv.read_modify_write_fpga_reg(reg, port_bitmap, val)

	def get_xcvr_interrupt_pins(self):
		"""Get xcvr interrupt pin state for all ports.
		Note: The pin state is inverted in pin register.

		Args:
			None.

		Returns:
			Integer representing bitmap of interrupt pin state for each port
			number starting from port 1 or None in case of error.
			Interrupt pin state description:
				1: Interrupt.
				0: No interrupt.
		"""
		return (~self.__get_xcvr_pin_state(reg_osfp_interrupt_sts)) & self.ports_mask

	def get_xcvr_present_pins(self):
		"""Get xcvr present pin state for all ports.
		Note: The pin state is inverted in pin register.

		Args:
			None.

		Returns:
			Integer representing bitmap of present pin state for each port
			number starting from port 1 or None in case of error.
			Present pin state description:
				1: Present.
				0: Not Present.
		"""
		return (~self.__get_xcvr_pin_state(reg_osfp_present_sts)) & self.ports_mask

	def get_xcvr_lowpower_pins(self):
		"""Get xcvr low power pin state for all ports.
		Note: The pin state is inverted in pin register.

		Args:
			None.

		Returns:
			Integer representing bitmap of low power pin state for each port
			number starting from port 1 or None in case of error.
			Low power pin state description:
				1: Low power mode.
				0: High power mode.
		"""
		return (~self.__get_xcvr_pin_state(reg_osfp_low_power)) & self.ports_mask

	def get_xcvr_reset_pins(self):
		"""Get xcvr reset pin state for all ports.
		Note: The pin state is inverted in pin register.

		Args:
			None.

		Returns:
			Integer representing bitmap of reset pin state for each port
			number starting from port 1 or None in case of error.
			Reset pin state description:
				1: Reset
				0: No Reset.
		"""
		return (~self.__get_xcvr_pin_state(reg_osfp_reset)) & self.ports_mask

	def set_xcvr_lowpower_pins(self, port_bitmap, state):
		"""Set xcvr low power pin state to `state` for each port number
		which is indicated by set bit position in `port_bitmap`
		Note: The pin state is inverted in pin register.

		Args:
			port_bitmap: integer representing bitmap of port numbers.
			state: integer representing the pin state to change for.
			low power pin state description:
				1: Low power mode.
				0: High power mode.

		Returns:
			None.
		"""
		self.__set_xcvr_pin_state(reg_osfp_low_power, port_bitmap, state^1)

	def set_xcvr_lowpower_pin(self, port, state):
		"""Set xcvr low power pin state to `state` for port number `port`
		Note: The pin state is inverted in pin register.

		Args:
			port: integer indicates port number to change its pin state.
			state: integer representing the pin state to change for.
			low power pin state description:
				1: Low power mode.
				0: High power mode.

		Returns:
			None.
		"""
		if 1 <= port <= self.ports_num:
			port_bitmap = 1 << (port-1)
			self.set_xcvr_lowpower_pins(port_bitmap, state)
		else:
			print("Error: port number {} is out of range[{},{}]".format(
				port, 1, self.ports_num))

	def set_xcvr_reset_pins(self, port_bitmap, state):
		"""Set xcvr reset pin state to `state` for each port number
		which is indicated by set bit position in `port_bitmap`
		Note: The pin state is inverted in pin register.

		Args:
			port_bitmap: integer representing bitmap of port numbers.
			state: integer representing the pin state to change for.
			reset pin state description:
				1: Reset.
				0: No Reset.

		Returns:
			None.
		"""
		self.__set_xcvr_pin_state(reg_osfp_reset, port_bitmap, state^1)

	def set_xcvr_reset_pin(self, port, state):
		"""Set xcvr reset pin state to `state` for port number `port`
		Note: The pin state is inverted in pin register.

		Args:
			port: integer indicates port number to change its pin state.
			state: integer representing the pin state to change for.
			reset pin state description:
				1: Reset.
				0: No Reset.

		Returns:
			None.
		"""
		if 1 <= port <= self.ports_num:
			port_bitmap = 1 << (port-1)
			self.set_xcvr_reset_pins(port_bitmap, state)
		else:
			print("Error: port number {} is out of range[{},{}]".format(
				port, 1, self.ports_num))
