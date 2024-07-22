#############################################################################
#
# Module contains an implementation of SONiC Platform Base API and
# provides the Chassis information which are available in the platform
#
#############################################################################

import os
import time

try:
    from sonic_platform_base.chassis_base import ChassisBase
    from .helper import APIHelper
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

NUM_FAN_TRAY = 5
NUM_FAN = 2
NUM_PSU = 1
NUM_LED = 1
NUM_RESET = 2
PORT_END = 16
NUM_COMPONENT = 4
POSITION_INDEX = 1

class Chassis(ChassisBase):
    """Platform-specific Chassis class"""

    def __init__(self):
        ChassisBase.__init__(self)

        self.__initialize_fan()
        self.__initialize_psu()
        self.__initialize_led()
        self.__initialize_reset()
        self.__initialize_thermals()
        self.__initialize_components()

    def __initialize_fan(self):
        from sonic_platform.fan_drawer import FanDrawer
        for fant_index in range(NUM_FAN_TRAY):
            fandrawer = FanDrawer(fant_index)
            self._fan_drawer_list.append(fandrawer)
            self._fan_list.extend(fandrawer._fan_list)

    def __initialize_psu(self):
        from sonic_platform.psu import Psu
        for index in range(0, NUM_PSU):
            psu = Psu(index)
            self._psu_list.append(psu)

    def __initialize_led(self):
        from sonic_platform.led import Led
        for index in range(0, NUM_LED):
            led = Led(index)
            self._led_list.append(led)

    def __initialize_reset(self):
        from sonic_platform.reset import Reset
        for index in range(0, NUM_RESET):
            reset = Reset(index)
            self._reset_list.append(reset)

    def __initialize_thermals(self):
        from sonic_platform.thermal import Thermal
        for index in range(0, Thermal.NUMBER_OF_THERMALS):
            thermal = Thermal(index)
            self._thermal_list.append(thermal)

    def __initialize_components(self):
        from sonic_platform.component import Component
        for index in range(0, NUM_COMPONENT):
            component = Component(index)
            self._component_list.append(component)

    def __is_host(self):
        return True

    def get_name(self):
        """
        Retrieves the name of the device
            Returns:
            string: The name of the device
        """
        return "N/A"

    def get_presence(self):
        """
        Retrieves the presence of the Chassis
        Returns:
            bool: True if Chassis is present, False if not
        """
        return True

    def get_status(self):
        """
        Retrieves the operational status of the device
        Returns:
            A boolean value, True if device is operating properly, False if not
        """
        return True

    def get_base_mac(self):
        """
        Retrieves the base MAC address for the chassis
        Returns:
            A string containing the MAC address in the format
            'XX:XX:XX:XX:XX:XX'
        """
        return ""

    def get_serial(self):
        """
        Retrieves the hardware serial number for the chassis
        Returns:
            A string containing the hardware serial number for this chassis.
        """
        return ""

    def get_system_eeprom_info(self):
        """
        Retrieves the full content of system EEPROM information for the chassis
        Returns:
            A dictionary where keys are the type code defined in
            OCP ONIE TlvInfo EEPROM format and values are their corresponding
            values.
        """
        return None

    def get_reboot_cause(self):
        """
        Retrieves the cause of the previous reboot

        Returns:
            A tuple (string, string) where the first element is a string
            containing the cause of the previous reboot. This string must be
            one of the predefined strings in this class. If the first string
            is "REBOOT_CAUSE_HARDWARE_OTHER", the second string can be used
            to pass a description of the reboot cause.
        """
        return "Unknown"

    def get_sfp(self, index):
        """
        Retrieves sfp represented by (1-based) index <index>
        Args:
            index: An integer, the index (1-based) of the sfp to retrieve.
            The index should be the sequence of a physical port in a chassis,
            starting from 1.
            For example, 1 for Ethernet0, 2 for Ethernet4 and so on.
        Returns:
            An object dervied from SfpBase representing the specified sfp
        """
        return None

    def get_thermal_manager(self):
        """
        Returns:
            ThermalManager
        """
        return None

    def set_thermal_policy_pause(self, timeout_minutes):
        """
        Returns:
            True|False
        """
        return None

    def get_change_event(self, timeout=0):
        """
        Returns:
            Change events
        """
        return False, {'sfp': {}}

    def is_replaceable(self):
        """
        Indicates whether this device is replaceable.
        Returns:
            bool: True if it is replaceable.
        """
        return False

    def get_model(self):
        """
        Retrieves the model number (or part number) of the device
        Returns:
            string: Model/part number of device
        """
        return "N/A"

    def get_num_fans(self):
        """
        Retrieves number of chassis fans
        Returns:
            integer: Number of fans
        """
        return len(self._fan_list)

    def get_all_fans(self):
        """
        Retrieves list of fans
        Returns:
            list: List of fans
        """
        return self._fan_list

    def get_num_fan_drawers(self):
        """
        Retrieves number of fan drawers
        Returns:
            integer: Number of fan drawers
        """
        return len(self._fan_drawer_list)

    def get_revision(self):
        """
        Retrieves the hardware revision number for the chassis
        Returns:
            A string containing the hardware revision number for this chassis.
        """
        return "N/A"

    def get_num_components(self):
        """
        Retrieves number of components
        Returns:
            integer: Number of components
        """
        return NUM_COMPONENT

    def get_status_led(self):
        return "UNKNOWN"

    def set_status_led(self, color):
        return False

    def initizalize_system_led(self):
        return True

    def get_position_in_parent(self):
        return POSITION_INDEX
