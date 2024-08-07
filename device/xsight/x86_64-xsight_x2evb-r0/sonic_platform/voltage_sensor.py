#############################################################################
#
# Module contains an implementation of SONiC Platform Base API and
# provides the voltage sensors information which are available in the platform
#
#############################################################################

try:
    from sonic_platform import bmc
    from sonic_platform_base.sensor_base import VoltageSensorBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class VoltageSensor(VoltageSensorBase):
    """Platform-specific Voltage sensor class"""

    def __init__(self, sensor_index=0):
        self.bmccmd = bmc.Bmc()
        self.index = sensor_index

    def get_value(self):
        """
        Retrieves measurement reported by sensor

        Returns:
            Sensor measurement
        """
        params = bmc.VOLTAGE_SENSOR_LIST[self.index]
        return int(1000 * float(self.bmccmd.power_ctrl_voltage(params[1], params[2], params[3])))

    def get_high_threshold(self):
        """
        Retrieves the high threshold of sensor

        Returns:
            High threshold
        """
        return "N/A"

    def get_low_threshold(self):
        """
        Retrieves the low threshold

        Returns:
            Low threshold
        """
        return "N/A"

    def set_high_threshold(self, value):
        """
        Sets the high threshold value of sensor

        Args:
            value: High threshold value to set

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        return False

    def set_low_threshold(self, value):
        """
        Sets the low threshold value of sensor

        Args:
            value: Value

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        return False

    def get_high_critical_threshold(self):
        """
        Retrieves the high critical threshold value of sensor

        Returns:
            The high critical threshold value of sensor
        """
        return "N/A"

    def get_low_critical_threshold(self):
        """
        Retrieves the low critical threshold value of sensor

        Returns:
            The low critical threshold value of sensor
        """
        return "N/A"

    def set_high_critical_threshold(self, value):
        """
        Sets the critical high threshold value of sensor

        Args:
            value: Critical high threshold Value

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        return False

    def set_low_critical_threshold(self, value):
        """
        Sets the critical low threshold value of sensor

        Args:
            value: Critial low threshold Value

        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        return False

    def get_minimum_recorded(self):
        """
        Retrieves the minimum recorded value of sensor

        Returns:
            The minimum recorded value of sensor
        """
        return "N/A"

    def get_name(self):
        """
        Retrieves the name of the device
            Returns:
            string: The name of the device
        """
        return bmc.VOLTAGE_SENSOR_LIST[self.index][0]

    def get_maximum_recorded(self):
        """
        Retrieves the maximum recorded value of sensor

        Returns:
            The maximum recorded value of sensor
        """
        return "N/A"

    def is_replaceable(self):
        """
        Retrieves whether device is replaceable
        returns:
            bool: True if it is replaceable
        """
        return False
