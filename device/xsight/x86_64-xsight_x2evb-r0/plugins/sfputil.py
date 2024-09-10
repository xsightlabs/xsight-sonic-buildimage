# sfputil.py
#
# Platform-specific SFP transceiver interface for SONiC
#

try:
    import time
    import string
    from ctypes import create_string_buffer
    from sonic_sfp.sfputilbase import SfpUtilBase
    from sonic_platform import xcvr_pins
except ImportError as e:
    raise ImportError("%s - required module not found" % str(e))

SFP_STATUS_INSERTED = '1'
SFP_STATUS_REMOVED = '0'

class SfpUtil(SfpUtilBase):
    """Platform-specific SfpUtil class"""

    PORT_START = 1
    PORT_END = 16

    BASE_VAL_PATH = "/sys/class/i2c-adapter/i2c-{0}/{1}-0050/"

    _port_to_eeprom_mapping = {}

    _port_to_i2c_mapping = {
        1:  2,
        2:  3,
        3:  4,
        4:  5,
        5:  6,
        6:  7,
        7:  8,
        8:  9,
        9:  10,
        10: 11,
        11: 12,
        12: 13,
        13: 14,
        14: 15,
        15: 16,
        16: 17,
    }

    @property
    def port_start(self):
        return self.PORT_START

    @property
    def port_end(self):
        return self.PORT_END

    @property
    def qsfp_port_start(self):
        return self.PORT_START

    @property
    def qsfp_port_end(self):
        return self.PORT_END

    @property
    def qsfp_ports(self):
        return list(range(self.PORT_START, self.PORT_END + 1))

    @property
    def port_to_eeprom_mapping(self):
        return self._port_to_eeprom_mapping

    def __init__(self):
        eeprom_path = '/sys/bus/i2c/devices/{0}-0050/eeprom'
        for x in range(self.port_start, self.port_end+1):
            self.port_to_eeprom_mapping[x] = eeprom_path.format(
                self._port_to_i2c_mapping[x])

        self.xcvrpins = xcvr_pins.XcvrPins(self.PORT_END)
        SfpUtilBase.__init__(self)

    def get_presence(self, port_num):
        if port_num < self.port_start or port_num > self.port_end:
            return False

        port_bit = 1 << (port_num - 1)
        val = self.xcvrpins.get_xcvr_present_pins()
        if val is not None:
            return (val & port_bit) == port_bit
        else:
             return False

    def get_low_power_mode(self, port_num):
        if port_num < self.port_start or port_num > self.port_end:
            return False

        port_bit = 1 << (port_num - 1)
        val = self.xcvrpins.get_xcvr_lowpower_pins()
        if val is not None:
            return (val & port_bit) == port_bit
        else:
            return False

    def set_low_power_mode(self, port_num, lpmode):
        if port_num < self.PORT_START or port_num > self.PORT_END:
            return False

        val = '1' if lpmode is True else '0'
        port_bit = 1 << (port_num - 1)
        self.xcvrpins.set_xcvr_lowpower_pins(port_bit, val)
        return True

    def reset(self, port_num):
        if port_num < self.PORT_START or port_num > self.PORT_END:
            return False

        port_bit = 1 << (port_num - 1)
        self.xcvrpins.set_xcvr_reset_pins(port_bit, 1)
        time.sleep(0.2)
        self.xcvrpins.set_xcvr_reset_pins(port_bit, 0)
        return True

    def get_transceiver_change_event(self):
        """
        TODO: This function need to be implemented
        when decide to support monitoring SFP(Xcvrd)
        on this platform.
        """
        raise NotImplementedError
