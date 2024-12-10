#############################################################################
#
# Thermal contains an implementation of SONiC Platform Base API and
# provides the thermal device status which are available in the platform
#
#############################################################################

try:
    from sonic_platform import bmc
    from .chassis import *
    from sonic_platform_base.thermal_base import ThermalBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

CHIP_THERMAL_OFFSET = bmc.NUM_THERMAL_MAIN_BOARD + bmc.NUM_THERMAL_CPU_BOARD

class Thermal(ThermalBase):
    """Platform-specific Thermal class"""

    def __init__(self, thermal_index=0):
        self.bmccmd = bmc.Bmc()
        self.index = thermal_index
        self._minimum = None
        self._maximum = None

    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal
        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125
        """
        val = ""

        if bmc.THERMAL_LIST[self.index][1] == "MAX6581":
            val = self.bmccmd.check_thermal_sensor(self.index + 1)
        elif bmc.THERMAL_LIST[self.index][1] == "TMP100":
            val = self.bmccmd.get_cpuboard_sensor()
        elif bmc.THERMAL_LIST[self.index][1] == "GLC":
            val = self.bmccmd.read_x2_thermal(self.index + 1 - CHIP_THERMAL_OFFSET)
        val = round(float(val or 0), 0)

        if self._minimum is None or self._minimum > val:
            self._minimum = val
        if self._maximum is None or self._maximum < val:
            self._maximum = val

        return val

    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal

        Returns:
            A float number, the high threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        val = self.bmccmd.get_thermal_thresholds(self.index, 1)
        return round(float(val or 0), 0)

    def get_low_threshold(self):
        """
        Retrieves the low threshold temperature of thermal

        Returns:
            A float number, the low threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        val = self.bmccmd.get_thermal_thresholds(self.index, 2)
        return round(float(val or 0), 0)

    def set_high_threshold(self, temperature):
        """
        Sets the high threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def set_low_threshold(self, temperature):
        """
        Sets the low threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def get_high_critical_threshold(self):
        """
        Retrieves the high critical threshold temperature of thermal

        Returns:
            A float number, the high critical threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        val = self.bmccmd.get_thermal_thresholds(self.index, 3)
        return round(float(val or 0), 0)

    def get_low_critical_threshold(self):
        """
        Retrieves the low critical threshold temperature of thermal

        Returns:
            A float number, the low critical threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        val = self.bmccmd.get_thermal_thresholds(self.index, 4)
        return round(float(val or 0), 0)

    def set_high_critical_threshold(self, temperature):
        """
        Sets the critical high threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def set_low_critical_threshold(self, temperature):
        """
        Sets the critical low threshold temperature of thermal

        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        raise NotImplementedError

    def get_minimum_recorded(self):
        """
        Retrieves the minimum recorded temperature of thermal

        Returns:
            A float number, the minimum recorded temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        if self._minimum is None:
            self.get_temperature()
        return self._minimum

    def get_maximum_recorded(self):
        """
        Retrieves the maximum recorded temperature of thermal

        Returns:
            A float number, the maximum recorded temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        if self._maximum is None:
            self.get_temperature()
        return self._maximum

    def get_name(self):
        """
        Retrieves the name of the thermal device
            Returns:
            string: The name of the thermal device
        """
        return bmc.THERMAL_LIST[self.index][0]

    def get_sensor_name(self):
        """
        Retrieves the name of the thermal device
            Returns:
            string: The name of the thermal device
        """
        return bmc.THERMAL_LIST[self.index][2]

    def get_model(self):
        """
        Retrieves the model of the thermal device
            Returns:
            string: The model of the thermal device
        """
        return bmc.THERMAL_LIST[self.index][1]

    def get_serial(self):
        """
        Retrieves the model of the thermal device
            Returns:
            string: The model of the thermal device
        """
        return "N/A"

    def is_replaceable(self):
        """
        Retrieves is the thermal device replaceable
            Returns:
            boolean: false
        """
        return False

    def get_presence(self):
        """
        Retrieves the presence of the Thermal
        Returns:
            bool: True if Thermal is present, False if not
        """
        return True

    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        return True

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device.
        Returns:
            integer: The 1-based relative physical position in parent device
        """
        return (self.index + 1)

