#############################################################################
#
# Thermal contains an implementation of SONiC Platform Base API and
# provides the thermal device status which are available in the platform
#
#############################################################################

import os
import os.path
import glob

try:
    from sonic_platform import bmc
    from .chassis import *
    from sonic_platform_base.thermal_base import ThermalBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Thermal(ThermalBase):
    """Platform-specific Thermal class"""
    NUMBER_OF_THERMALS = 8
    MAIN_BOARD_TEMP_SENSORS_OFFSET = 0
    CPU_BOARD_TEMP_SENSORS_OFFSET = 7
    THERMAL_NAME_LIST = []

    def __init__(self, thermal_index=0):
        self.bmccmd = bmc.Bmc()
        self.index = thermal_index

        # Add thermal name
        self.THERMAL_NAME_LIST.append("Temp sensor 1")
        self.THERMAL_NAME_LIST.append("Temp sensor 2")
        self.THERMAL_NAME_LIST.append("Temp sensor 3")
        self.THERMAL_NAME_LIST.append("Temp sensor 4")
        self.THERMAL_NAME_LIST.append("Temp sensor 5")
        self.THERMAL_NAME_LIST.append("Temp sensor 6")
        self.THERMAL_NAME_LIST.append("Temp sensor 7")
        self.THERMAL_NAME_LIST.append("Temp sensor 8")

    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal
        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125
        """
        temp = None
        if self.index < Thermal.CPU_BOARD_TEMP_SENSORS_OFFSET:
            temp = float(self.bmccmd.check_thermal_sensor(self.index + 1))
        elif self.index == Thermal.CPU_BOARD_TEMP_SENSORS_OFFSET:
            temp = float(int(float(self.bmccmd.get_cpuboard_sensor())))
        return temp

    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal
        Returns:
            A float number, the high threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        return "N/A"

    def set_high_threshold(self, temperature):
        """
        Sets the high threshold temperature of thermal
        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        return False

    def get_name(self):
        """
        Retrieves the name of the thermal device
            Returns:
            string: The name of the thermal device
        """
        return self.THERMAL_NAME_LIST[self.index]

    def get_sensor_name(self):
        """
        Retrieves the name of the thermal device
            Returns:
            string: The name of the thermal device
        """
        name = ""
        if self.index < Thermal.CPU_BOARD_TEMP_SENSORS_OFFSET:
            name = bmc.MAIN_BOARD_THERMAL_SENSOR_NAMES[self.index]
        elif self.index == Thermal.CPU_BOARD_TEMP_SENSORS_OFFSET:
            name = bmc.CPU_BOARD_THERMAL_SENSOR_NAMES[0]
        return name

    def get_model(self):
        """
        Retrieves the model of the thermal device
            Returns:
            string: The model of the thermal device
        """
        model = ""
        if self.index < Thermal.CPU_BOARD_TEMP_SENSORS_OFFSET:
            model = "MAX6581"
        elif self.index == Thermal.CPU_BOARD_TEMP_SENSORS_OFFSET:
            model = "TMP100"
        return model

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

