#############################################################################
# Edgecore
#
# Thermal contains an implementation of SONiC Platform Base API and
# provides the thermal device status which are available in the platform
#
#############################################################################

import os
import os.path
import glob

try:
    from sonic_platform_base.thermal_base import ThermalBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Thermal(ThermalBase):
    """Platform-specific Thermal class"""
    ZONE_CRITICAL_TEMPERATURE = 80
    THERMAL_NAME_LIST = []
    SYSFS_PATH = "/sys/bus/i2c/devices"

    def __init__(self, thermal_index=0):
        self.index = thermal_index
        # Add thermal name
        self.THERMAL_NAME_LIST.append("Temp sensor 1")
        self.THERMAL_NAME_LIST.append("Temp sensor 2")
        self.THERMAL_NAME_LIST.append("Temp sensor 3")
        self.THERMAL_NAME_LIST.append("Temp sensor 4")
        self.THERMAL_NAME_LIST.append("Temp sensor 5")
        self.THERMAL_NAME_LIST.append("Temp sensor 6")
        self.THERMAL_NAME_LIST.append("Temp sensor 7")

        # Set hwmon path
        i2c_path = {
            0: "18-0048/hwmon/hwmon*/",
            1: "18-0049/hwmon/hwmon*/",
            2: "18-004a/hwmon/hwmon*/",
            3: "18-004b/hwmon/hwmon*/",
            4: "18-004d/hwmon/hwmon*/",
            5: "18-004e/hwmon/hwmon*/",
            6: "18-004f/hwmon/hwmon*/",
        }.get(self.index, None)

        self.hwmon_path = "{}/{}".format(self.SYSFS_PATH, i2c_path)
        self.ss_key = self.THERMAL_NAME_LIST[self.index]
        self.ss_index = 1

    def __read_txt_file(self, file_path):
        for filename in glob.glob(file_path):
            try:
                with open(filename, 'r') as fd:
                    data =fd.readline().rstrip()
                    return data
            except IOError as e:
                pass

        return None

    def __get_temp(self, temp_file):
        temp_file_path = os.path.join(self.hwmon_path, temp_file)
        raw_temp = self.__read_txt_file(temp_file_path)
        if raw_temp is not None:
            return float(raw_temp)/1000
        else:
            return 0


    def __set_threshold(self, file_name, temperature):
        temp_file_path = os.path.join(self.hwmon_path, file_name)
        for filename in glob.glob(temp_file_path):
            try:
                with open(filename, 'w') as fd:
                    fd.write(str(temperature))
                return True
            except IOError as e:
                print("IOError")


    def get_temperature(self):
        """
        Retrieves current temperature reading from thermal
        Returns:
            A float number of current temperature in Celsius up to nearest thousandth
            of one degree Celsius, e.g. 30.125
        """
        temp_file = "temp{}_input".format(self.ss_index)
        return self.__get_temp(temp_file)

    def get_high_threshold(self):
        """
        Retrieves the high threshold temperature of thermal
        Returns:
            A float number, the high threshold temperature of thermal in Celsius
            up to nearest thousandth of one degree Celsius, e.g. 30.125
        """
        temp_file = "temp{}_max".format(self.ss_index)
        return self.__get_temp(temp_file)

    def set_high_threshold(self, temperature):
        """
        Sets the high threshold temperature of thermal
        Args :
            temperature: A float number up to nearest thousandth of one degree Celsius,
            e.g. 30.125
        Returns:
            A boolean, True if threshold is set successfully, False if not
        """
        temp_file = "temp{}_max".format(self.ss_index)
        temperature = temperature *1000
        self.__set_threshold(temp_file, temperature)

        return True

    def get_name(self):
        """
        Retrieves the name of the thermal device
            Returns:
            string: The name of the thermal device
        """
        return self.THERMAL_NAME_LIST[self.index]

    def get_presence(self):
        """
        Retrieves the presence of the Thermal
        Returns:
            bool: True if Thermal is present, False if not
        """
        temp_file = "temp{}_input".format(self.ss_index)
        temp_file_path = os.path.join(self.hwmon_path, temp_file)
        raw_txt = self.__read_txt_file(temp_file_path)
        if raw_txt is not None:
            return True
        else:
            return False

    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """

        file_str = "temp{}_input".format(self.ss_index)
        file_path = os.path.join(self.hwmon_path, file_str)
        raw_txt = self.__read_txt_file(file_path)
        if raw_txt is None:
            return False
        else:
            return int(raw_txt) != 0

    @classmethod
    def set_thermal_algorithm_status(cls, status, force=True):
        """
        Enable/disable kernel thermal algorithm.
        When enable kernel thermal algorithm, kernel will adjust fan speed
        according to thermal zones temperature. Please note that kernel will
        only adjust fan speed when temperature across some "edge", e.g temperature
        changes to exceed high threshold.
        When disable kernel thermal algorithm, kernel no longer adjust fan speed.
        We usually disable the algorithm when we want to set a fix speed. E.g, when 
        a fan unit is removed from system, we will set fan speed to 100% and disable 
        the algorithm to avoid it adjust the speed.

        Returns:
            True if thermal algorithm status changed.

        TODO: required kernel implementation
        """
        if not force and cls.thermal_algorithm_status == status:
            return False

        cls.thermal_algorithm_status = status
        # TODO Need to switch kernel algorithm according to status
        print("Thermal:set_thermal_algorithm_status - Kernel thermal algorithm: {}".format(str(cls.thermal_algorithm_status)))

        return True

    @classmethod
    def get_min_amb_temperature(cls):
        """
        Calculating ambient temperature inside the box,
        Returns:
            float - ambient temperature
        TODO: temperature calculation need to be reviewed after receiving temperature profiling from hardware vendor
        """
        import sonic_platform.platform
        import sonic_platform_base.sonic_sfp.sfputilhelper
        ambient = None
        platform_chassis = sonic_platform.platform.Platform().get_chassis()
        if platform_chassis is not None:
            thermals_num = platform_chassis.get_num_thermals()
            ambient = 0.0
            print("Thermal: Got {} Thermal Objects".format(thermals_num))
            for thermal_ins in platform_chassis.get_all_thermals():
                ambient += thermal_ins.get_temperature()
            ambient /= thermals_num
        else:
            print("Thermal: Chassis not available !")
        print("Thermal:get_min_amb_temperature Returns: {}".format(ambient))
        return ambient

    @classmethod
    def check_thermal_zone_temperature(cls):
        """
        Check thermal zone current temperature with normal temperature

        Returns:
            True if all thermal zones current temperature less or equal than normal temperature
        TODO: Check if need some special temperature profiling per each sensor
        TODO: Pass over temeperatues on modules
        """
        # Check Inbox thermperatures
        import sonic_platform.platform
        platform_chassis = sonic_platform.platform.Platform().get_chassis()
        if platform_chassis is not None:
            thermals_num = platform_chassis.get_num_thermals()
            #print("Thermal: Got {} Thermals Objects".format(thermals_num))
            for thermal_ins in platform_chassis.get_all_thermals():
                if (cls.ZONE_CRITICAL_TEMPERATURE <= thermal_ins.get_temperature()):
                    #print("Thermal: Critical temperature on {}".format(thermal_ins.get_name()))
                    return False
        else:
            print("Thermal: Chassis not available !")

        print("Thermal:check_thermal_zone_temperature: All temperatures look OK")
        return True

