#############################################################################
#
# Module contains an implementation of SONiC Platform Base API and
# provides the PSUs status which are available in the platform
#
#############################################################################

import os.path

try:
    from bmc import bmc
    from sonic_platform_base.psu_base import PsuBase
    from .helper import APIHelper
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

PSU_NAME_LIST = ["PSU-1"]

class Psu(PsuBase):
    """Platform-specific Psu class"""

    def __init__(self, psu_index=0):
        PsuBase.__init__(self)
        self.index = psu_index
        self.bmccmd = bmc.Bmc()

    def get_voltage(self):
        """
        Retrieves current PSU voltage output
        Returns:
            A float number, the output voltage in volts,
            e.g. 12.1
        """
        return float(self.bmccmd.psup_voltage())

    def get_current(self):
        """
        Retrieves present electric current supplied by PSU
        Returns:
            A float number, the electric current in amperes, e.g 15.4
        """
        return float(self.bmccmd.psup_current())

    def get_power(self):
        """
        Retrieves current energy supplied by PSU
        Returns:
            A float number, the power in watts, e.g. 302.6
        """
        return float(self.bmccmd.psup_power())

    def set_status_led(self, color):
        """
        Sets the state of the PSU status LED
        Args:
            color: A string representing the color with which to set the PSU status LED
                   Note: Only support green, amber and off
        Returns:
            bool: True if status LED state is set successfully, False if not
        """
        return False

    def get_status_led(self):
        """
        Gets the state of the PSU status LED
        Returns:
            A string, one of the predefined STATUS_LED_COLOR_* strings above
        """
        return "N/A"

    def get_temperature(self):
        """
        Retrieves current temperature reading from PSU
        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125
        """
        return False #Not supported

    def get_temperature_high_threshold(self):
        """
        Retrieves the high threshold temperature of PSU
        Returns:
            A float number, the high threshold temperature of PSU in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        return False #Not supported

    def get_voltage_high_threshold(self):
        """
        Retrieves the high threshold PSU voltage output
        Returns:
            A float number, the high threshold output voltage in volts,
            e.g. 12.1
        """
        return False #Not supported

    def get_voltage_low_threshold(self):
        """
        Retrieves the low threshold PSU voltage output
        Returns:
            A float number, the low threshold output voltage in volts,
            e.g. 12.1
        """
        return False #Not supported

    def get_name(self):
        """
        Retrieves the name of the device
            Returns:
            string: The name of the device
        """
        return PSU_NAME_LIST[self.index]

    def get_presence(self):
        """
        Retrieves the presence of the PSU
        Returns:
            bool: True if PSU is present, False if not
        """
        return True

    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        return True

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device
        Returns:
            string: Model/part number of device
        """
        return "DPS-3000AB"

    def get_serial(self):
        """
        Retrieves the serial number of the device
        Returns:
            string: Serial number of device
        """
        return "N/A"

    def is_replaceable(self):
        """
        Retrieves whether device is replaceable
        returns:
            bool: True if it is replaceable
        """
        return True

    def get_powergood_status(self):
        """
        Retrieves the powergood status of PSU
        Returns:
            A boolean, True if PSU has stablized its output voltages and passed all
            its internal self-tests, False if not.
        """
        return self.get_status()

    def get_maximum_supplied_power(self):
        """
        Retrieves maximum supplied power of PSU
        Returns:
            float: Power in watts
        """
        return self.get_power()

    def get_revision(self):
        """
        Retrieves the hardware revision of the device

        Returns:
            string: Revision value of device
        """
        return self.get_serial()

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device.
        Returns:
            integer: The 1-based relative physical position in parent device
        """
        return (self.index + 1)

