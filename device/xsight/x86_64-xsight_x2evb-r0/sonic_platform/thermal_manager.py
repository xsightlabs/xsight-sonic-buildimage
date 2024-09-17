import os
from sonic_platform import bmc
from sonic_platform_base.sonic_thermal_control.thermal_manager_base import ThermalManagerBase
from sonic_platform_base.sonic_thermal_control.thermal_policy import ThermalPolicy
from .helper import APIHelper

class ThermalManager(ThermalManagerBase):
    bmccmd = bmc.Bmc()

    @classmethod
    def initialize(cls):
        """
        Initialize thermal manager, including register thermal condition types and thermal action types
        and any other vendor specific initialization.
        :return:
        """
        cls.bmccmd.set_monitor(1)

    @classmethod
    def deinitialize(cls):
        """
        Destroy thermal manager, including any vendor specific cleanup. The default behavior of this function
        is a no-op.
        :return:
        """
        cls.bmccmd.set_monitor(0)

    @classmethod
    def stop(cls):
        """
        Stop thermal manager.
        :return:
        """
        pass

    @classmethod
    def start_thermal_control_algorithm(cls):
        """
        Start thermal control algorithm

        Returns:
            bool: True if start succeeded. False - if failed. 
        """
        return False

    @classmethod
    def stop_thermal_control_algorithm(cls):
        """
        Stop thermal control algorithm

        Returns:
            bool: True if start succeeded. False - if failed.
        """
        return False

    @classmethod
    def load(cls, policy_file_name):
        """
        Load all thermal policies from JSON policy file.
        :param policy_file_name: Path of JSON policy file.
        :return:
        """
        pass

    @classmethod
    def run_policy(cls, chassis):
        """
        Collect thermal information, run each policy, if one policy matches, execute the policy's action.
        :param chassis: The chassis object.
        :return:
        """
        pass

    @classmethod
    def init_thermal_algorithm(cls, chassis):
        """
        Initialize thermal algorithm according to policy file.
        :param chassis: The chassis object.
        :return:
        """
        pass

    @classmethod
    def pause_thermal_algorithm(cls, timeout_minutes=1):
        """
        Pause thermal policy with timeout in minutes

        Returns:
            bool: True, if succeeded to place pause request. False - if failed.
        """
        return False

    @classmethod
    def _add_private_thermal_policy(cls):
        pass
