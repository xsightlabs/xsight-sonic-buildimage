#############################################################################
#
# Module contains an implementation of SONiC Platform Base API and
# provides the fan status which are available in the platform
#
#############################################################################

try:
    from sonic_platform import bmc
    from sonic_platform_base.fan_base import FanBase
    from sonic_platform import platform
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

TRAY_FANSPEED_TOLERANCE = 25

class Fan(FanBase):
    """Platform-specific Fan class"""

    def __init__(self, fan_tray_index, fan_index=0, is_psu_fan=False, psu_index=0):
        self.bmccmd = bmc.Bmc()
        self.fan_index = fan_index
        self.fan_tray_index = fan_tray_index
        self.is_psu_fan = is_psu_fan
        self.psu_index = psu_index

        FanBase.__init__(self)

    def get_name(self):
        """
        Retrieves fan name
        Returns:
            A string with fan name either from fan tray or from psu
        """
        return "FanTray {} fan {}".format(self.fan_tray_index, self.fan_index)

    def get_model(self):
        """
        Retrieves the fan model
        Returns:
            string: The model of the device
        """
        return "R40W12BGNL9-07A063"

    def get_serial(self):
        """
        Retrieves the fan serial
        Returns:
            string: The serial of the device
        """
        return "N/A"

    def is_replaceable(self):
        """
        Indicate whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return True

    def get_direction(self):
        """
        Retrieves the direction of fan
        Returns:
            A string, either FAN_DIRECTION_INTAKE or FAN_DIRECTION_EXHAUST
            depending on fan direction
        """
        return "N/A"

    def get_speed(self):
        """
        Retrieves the speed of fan as a percentage of full speed
        Returns:
            An integer, the percentage of full fan speed, in the range 0 (off)
                 to 100 (full speed)
        """
        return int(self.bmccmd.read_fan_speed() or 0)

    def get_target_speed(self):
        """
        Retrieves the target (expected) speed of the fan
        Returns:
            An integer, the percentage of full fan speed, in the range 0 (off)
                 to 100 (full speed)
        """
        return int(self.bmccmd.read_fan_speed() or 0)

    def get_speed_tolerance(self):
        """
        Retrieves the speed tolerance of the fan
        Returns:
            An integer, the percentage of variance from target speed which is
                 considered tolerable
        """
        return TRAY_FANSPEED_TOLERANCE

    def set_speed(self, speed):
        """
        Sets the fan speed
        Args:
            speed: An integer, the percentage of full fan speed to set fan to,
                   in the range 0 (off) to 100 (full speed)
        Returns:
            A boolean, True if speed is set successfully, False if not

        """
        self.bmccmd.set_fan_mode(int(speed))

    def get_presence(self):
        """
        Retrieves the presence of the FAN
        Returns:
            bool: True if FAN is present, False if not
        """
        return self.bmccmd.get_fan_exist(self.fan_index + 1)

    def get_status(self):
        """
        Returns Fan Status. Called in _refresh_fan_status thermalctld's function
        Returns:
            bool: True if status Ok, False if not
        TODO: get_status required implementation !
        Always return true as workaround for error in syslog.
        """
        return True

    def get_position_in_parent(self):
        """
        Retrieves 1-based relative physical position in parent device.
        Returns:
            integer: The 1-based relative physical position in parent device
        """
        if self.is_psu_fan:
            return (self.psu_index + 1)
        else:
            return (self.fan_index + 1)

