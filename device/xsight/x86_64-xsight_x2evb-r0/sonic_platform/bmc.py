# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 Xsightlabs Ltd.

import subprocess
import socket
import json
import re

# Notes
# 1. The main board schematic version refered in this file is REV. 1
# 2. The cpu board schematic version refered in this file is REV. 1

NUM_FAN_TRAY = 5
NUM_PSU = 1
NUM_VOLTAGE_SENSOR = 17
NUM_CURRENT_SENSOR = 17
NUM_COMPONENT = 4
NUM_THERMAL_MAIN_BOARD = 7
NUM_THERMAL_CPU_BOARD = 1
NUM_THERMAL_CHIP = 3
NUM_THERMAL = NUM_THERMAL_MAIN_BOARD + NUM_THERMAL_CPU_BOARD + NUM_THERMAL_CHIP

PSU_LIST = ["PSU-1"]

# Component name, Component description
COMPONENT_LIST= [
   ("BIOS", "Basic Input/Output System"),
   ("ONIE", "Open Network Install Environment"),
   ("BMC" , "Baseboard Management Controller"),
   ("FPGA", "Field Programmable Gate Array")
]

# Thermal name, Model, Sensor name
THERMAL_LIST= [
   ("Temp sensor 1", "MAX6581", "Chip Diode"),
   ("Temp sensor 2", "MAX6581", "Input Air"),
   ("Temp sensor 3", "MAX6581", "OSFP"),
   ("Temp sensor 4", "MAX6581", "East Side"),
   ("Temp sensor 5", "MAX6581", "West Side"),
   ("Temp sensor 6", "MAX6581", "Output Air 1"),
   ("Temp sensor 7", "MAX6581", "Output Air 2"),
   ("Temp sensor 8", "TMP100" , "CPU Board"),
   ("ASIC sensor 1", "GLC"    , "GLC0"),
   ("ASIC sensor 2", "GLC"    , "GLC1"),
   ("ASIC sensor 3", "GLC"    , "GLC3")
]

# Sensor name, Device id, FPGA client, Page number
CURRENT_SENSOR_LIST = [
    ("VDDCORE"    , 0x40, 3, 0),
    ("VDDSD"      , 0x42, 3, 0),
    ("VDDH_1_2_0" , 0x44, 3, 0),
    ("VDDH_2_3_0" , 0x46, 3, 0),
    ("VDDL_1_2_0" , 0x48, 3, 0),
    ("VDDL_2_3_0" , 0x4A, 3, 0),
    ("VDDH_1_2_1" , 0x44, 3, 1),
    ("VDDH_2_3_1" , 0x46, 3, 1),
    ("VDDL_1_2_1" , 0x48, 3, 1),
    ("VDDL_2_3_1" , 0x4A, 3, 1),
    ("OSFP_0TO3"  , 0x40, 6, 0),
    ("OSFP_4TO7"  , 0x41, 6, 0),
    ("OSFP_8TO11" , 0x42, 6, 0),
    ("OSFP_12TO15", 0x43, 6, 0),
    ("GPWR_3V3"   , 0x44, 6, 0),
    ("GPWR_1V8"   , 0x45, 6, 0),
    ("AUX_PWR_3V3", 0x46, 6, 0)
]

# Sensor name, Device id, FPGA client, Page number
VOLTAGE_SENSOR_LIST = [
    ("VDDCORE"    , 0x40, 3, 0),
    ("VDDSD"      , 0x42, 3, 0),
    ("VDDH_1_2_0" , 0x44, 3, 0),
    ("VDDH_2_3_0" , 0x46, 3, 0),
    ("VDDL_1_2_0" , 0x48, 3, 0),
    ("VDDL_2_3_0" , 0x4A, 3, 0),
    ("VDDH_1_2_1" , 0x44, 3, 1),
    ("VDDH_2_3_1" , 0x46, 3, 1),
    ("VDDL_1_2_1" , 0x48, 3, 1),
    ("VDDL_2_3_1" , 0x4A, 3, 1),
    ("OSFP_0TO3"  , 0x40, 6, 0),
    ("OSFP_4TO7"  , 0x41, 6, 0),
    ("OSFP_8TO11" , 0x42, 6, 0),
    ("OSFP_12TO15", 0x43, 6, 0),
    ("GPWR_3V3"   , 0x44, 6, 0),
    ("GPWR_1V8"   , 0x45, 6, 0),
    ("AUX_PWR_3V3", 0x46, 6, 0)
]

class Bmc:
    """
    A class used to send JSON RPC commands to BMC.

    Attributes:
        sock: socket instance for BMC JSON RPC client connection.
    """

    def __init__(self):
        """Create and open socket connection.

        Args:
            None.

        Returns:
            None.
        """
        port = 9087
        process = subprocess.run('hostname', shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        hostname = process.stdout.rstrip()
        if "host" in hostname:
            hostname = hostname.replace("host", "bmc")
        elif "evb" in hostname:
            hostname = hostname.replace("evb", "bmc")
        else:
            hostname = ""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.settimeout(10)
            self.sock.connect((hostname, port))
        except Exception as e:
            print("Error: Failed to connect to socket")
            raise Exception(str(e))

    def __del__(self):
        """Close socket connection.

        Args:
            None.

        Returns:
            None.
        """
        self.sock.close()

    def __extract_number_from_string(self, input_str, str_idx):
        """Get a number (integer, float, hex) in string format from the input
        string, using the information of str_idx.

        Args:
            input_str: input string.
            str_idx: integer representing the index of the number in the input string.

        Returns:
            String representing the number that has been extracted from
            the input string, or empty string in case of error.
        """
        ret_str = ""
        reg_pattern = r"0[xX][0-9a-fA-F]+|\d+.\d+.\d+|[-+]?\d*\.?\d+|[-+]?\d+"
        jsonobj = json.loads(input_str)
        str_list = re.findall(reg_pattern, str(jsonobj['result']))
        if len(str_list) >= str_idx:
            ret_str = str_list[str_idx - 1]
        else:
            print("Error: Failure in expected list length ", len(str_list))
        return ret_str

    def __extract_substring_from_string(self, input_str, str_idx, str_delim):
        """Get a string from the input string, using the information of str_idx
        and str_delim.

        Args:
            input_str: string of JSON RPC response.
            str_idx: integer representing the splited string part to return.
            str_delim: string representing a delimiter to split the input string.

        Returns:
            String that has been extracted from the input string, or empty string
            in case of error.
        """
        ret_str = ""
        jsonobj = json.loads(input_str)
        str_list = jsonobj['result'].split(str_delim)
        if len(str_list) >= str_idx:
            ret_str = str_list[str_idx - 1]
        else:
            print("Error: Failure in expected list length ", len(str_list))
        return ret_str

    def __build_and_send_json_rpc(self, method, params):
        """Build and send JSON string to BMC JSON RPC server.

        Args:
            method: string representing method name for JSON string.
            params: list representing parameter list for JSON string.

        Returns:
            String of BMC JSON RPC response, or empty string in case of error.

        Notes:
            The JSON RPC string can be reviewed on the BMC repo at:
            https://bbk.xsightlabs.com/projects/XB/repos/vbmc/browse/r0a_commands.sh
        """
        buffer = b''
        json_dict = {"method": method, "params": params}
        json_bytes = json.dumps(json_dict).encode()
        try:
            send_len = self.sock.send(json_bytes)
            if len(json_bytes) == send_len:
                # Looks for end of JSON response string
                while b'\n}\n' not in buffer:
                    rec_buf = self.sock.recv(1024)
                    buffer += rec_buf
                    # Indicates that the socket has disconnected.
                    if not rec_buf:
                        break
        except Exception as e:
            print("Error: Failed to send message over socket")
            raise Exception(str(e))
        ret_str = buffer.decode()
        return ret_str

    def __is_valid_current_type(self, current_type):
        """Check if input current type is valid.

        Args:
            current_type: integer representing the current sample type.
                Valid options:
                0 - iout, output current
                1 - max, highest output current
                2 - min, lowest output current
        Returns:
            Boolean representing input current_type validity.
                False - current_type is invalid.
                True - current_type is valid.
        """
        ret_val = True
        if current_type not in [0, 1, 2]:
            print("Error: current_type {} is out of range [0 - 2]".format(current_type))
            ret_val = False
        return ret_val

    def __is_valid_device_id_combination(self, device_id, fpga_client, page):
        """Check if input device_id combination is valid. There are a specific
        options for device_id (which is I2C slave address) with fpga_client
        (which is FPGA I2CM_IND master) and page number (which is PMBus page number).
        See Notes for more information.

        Args:
            device_id: integer representing I2C slave address.
                please see Notes below for device ID list.
            fpga_client: integer representing fpga client (which is act as
                I2C master) of FPGA I2CM_IND block. The supported
                fpga clients are detailed in the following list:
                3 - Alon power
                6 - OSFP + general power
            page: integer representing the page number of device's PMBus.

        Returns:
            Boolean representing input device_id combination validity.
                False - device_id combination is invalid.
                True - device_id combination is valid.

        Notes:
            1. The FPGA I2CM_IND registers can be reviewed at:
               http://soc.xsight.ent/app/index.cgi?
            2. MB number is main board schematic component number.
            3. MB name is the main board schematic component name.
            4. For main board schematic version please refer to Notes
               at the top of this file.
            5. The device id combinations are detailed in the following list:
               fpga_client  device_id  page  MB name      MB number
               -----------  ---------  ----  -------      ---------
               3            0x40       0     VDD_CORE     U202
               3            0x42       0     SD_VDD       U202
               3            0x44       0/1   VDDH_1_2     U177
               3            0x46       0/1   VDDH_2_3     U177
               3            0x48       0/1   VDDL_1_2     U180
               3            0x4A       0/1   VDDL_2_3     U180
               6            0x40       0     OSFP_0TO3    U175
               6            0x41       0     OSFP_4TO7    U174
               6            0x42       0     OSFP_8TO11   U176
               6            0x43       0     OSFP_12TO15  U137
               6            0x44       0     GPWR_3V3     U179
               6            0x45       0     GPWR_1V8     U182
               6            0x46       0     AUX_PWR_3V3  U203
        """
        ret_val = True
        dev_id_combination_dict = {3: {0: [0x40, 0x42, 0x44, 0x46, 0x48, 0x4A],
                        1: [0x44, 0x46, 0x48, 0x4A]},
                    6: {0: [0x40, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46]}}

        try:
            dev_id_list = dev_id_combination_dict[fpga_client][page]
        except KeyError:
            dev_id_list = []

        if not device_id in dev_id_list:
            print("Error: Wrong arguments fpga_client {} device_id {} page {}"
                .format(hex(device_id), fpga_client, page))
            ret_val = False
        return ret_val

    def is_bmc_fpga_vers_higher_than(self, bmc_ver_min, fpga_ver_min):
        ver = int(self.get_bmc_version().replace('.', '').ljust(3, '0'))
        ver_min = int(bmc_ver_min.replace('.', '').ljust(3, '0'))
        if ver < ver_min:
            return False

        ver = int(self.get_fpga_version(), 16)
        ver_min = int(fpga_ver_min, 16)
        if ver < ver_min:
            return False

        return True

    def sys_led_ctrl(self, red, green, blue):
        """Set system led RGB (Red, Green, Blue) colors.

        Args:
            red: integer of 0/1.
            green: integer of 0/1.
            blue: integer of 0/1.

       Returns:
            A boolean value, True if the operation succeeded, False if not.

        Notes:
            The system led color is selected in FPGA registers at:
            http://soc.xsight.ent/app/viewItem.cgi?itm=reg&p=1020&b=2&&r=27&
        """
        ret_val = False
        if (red in [0, 1]) and (green in [0, 1]) and (blue in [0, 1]):
            params = [red, green, blue]
            resp_str = self.__build_and_send_json_rpc("sys_led_ctrl", params)
            if ("red" in resp_str) and ("green" in resp_str) and ("blue" in resp_str):
                ret_val = True
        else:
            print("Error: RGB [{},{},{}] is out of range [0 - 1]".format(red, green, blue))
        return ret_val

    def set_sys_led_color(self, color):
        """Set system led color to predefined colors options.

        Args:
            color: integer of the following options:
                0 - Red.
                1 - Green.
                2 - Blue.
                3 - Amber.

        Returns:
            None.

        Notes:
            The system led color is selected in FPGA registers at:
            http://soc.xsight.ent/app/viewItem.cgi?itm=reg&p=1020&b=2&&r=27&
        """
        if 0 <= color <= 3:
            if color == 0:
                red, green, blue = 1, 0, 0
            if color == 1:
                red, green, blue = 0, 1, 0
            if color == 2:
                red, green, blue = 0, 0, 1
            if color == 3:
                red, green, blue = 1, 1, 0
            ret_val = self.sys_led_ctrl(red, green, blue)
        else:
            print("Error: color {} is out of range [0 - 3]".format(color))
            ret_val = False
        return ret_val

    def sys_led_status(self):
        """Read system LED color.

        Args:
            None.

        Returns:
            String of system LED color.
        """
        color = "UNKNOWN"
        if not self.is_bmc_fpga_vers_higher_than("2.6.9", "0x30E"):
            return color

        resp_str = self.__build_and_send_json_rpc("sys_led_status", [])
        red = 1 if "ON" in self.__extract_substring_from_string(resp_str, 2, ": ") else 0
        blue = 1 if "ON" in self.__extract_substring_from_string(resp_str, 3, ": ") else 0
        green = 1 if "ON" in self.__extract_substring_from_string(resp_str, 4, ": ") else 0

        if (red == 1) and (green == 0) and (blue == 0):
            color = "red"
        elif (red == 0) and (green == 1) and (blue == 0):
            color = "green"
        elif (red == 0) and (green == 0) and (blue == 1):
            color = "blue"
        elif (red == 1) and (green == 1) and (blue == 0):
            color = "amber"

        return color

    def psup_current(self):
        """Read PSUP current in Amper units.

        Args:
            None.

        Returns:
            String of float number representing PSUP current or empty string
            in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("psup_current", [])
        return self.__extract_number_from_string(resp_str, 1)

    def power_ctrl_current(self, device_id, fpga_client, page, current_type, sample_num):
        """Read current in Amper units from PMBus devices.

        Args:
            device_id: integer representing I2C slave address.
            fpga_client: integer representing fpga client (which is act
                as I2C master) of FPGA I2CM_IND block.
            page: integer representing the page number of device's PMBus.
            current_type: integer representing the current sample type.
            sample_num: integer representing number of sample to take.

        Returns:
            String of float number representing the device's current
            sample in Amper units or empty string in case of error.

        Notes:
            1. For valid device_id/fpga_client/page combination please
               refer to the docstring section of the function
               '__is_valid_device_id_combination'
            2. For valid current_type options please refer to the
               docstring section of the function '__is_valid_current_type'
        """
        if (sample_num <= 0):
            print("Error: sample_num {} must be positive".format(sample_num))
            return ""

        if not self.__is_valid_current_type(current_type):
            return ""

        if not self.__is_valid_device_id_combination(device_id, fpga_client, page):
            return ""

        params = [device_id, fpga_client, page, current_type, sample_num]
        resp_str = self.__build_and_send_json_rpc("power_ctrl_current", params)
        return self.__extract_number_from_string(resp_str, 4)

    def set_fan_mode(self, percent):
        """Set all box FANs mode to RPM of 0%-100%.

        Args:
            percent: integer representing the FAN mode percentage in
                the range of [0 - 100].

        Returns:
            A boolean value, True if the operation succeeded, False if not.

        Notes:
            This function changed the fan speed both in run time and in BMC's
            configuration file to keep the changes after BMC reboot.
            The BMC has a method to set the fan speed in runtime to both `regular`
            and `hot` modes, when we use this method the fan speed for `hot` mode
            is always to 100%.
        """
        if (percent < 0) or (percent > 100):
            print("Error: percent {} is out of range [0 - 100]".format(percent))
            return False

        resp_str = self.__build_and_send_json_rpc("set_default_fan_values", [percent, 100])
        if "done" not in resp_str:
            return False

        resp_str = self.__build_and_send_json_rpc("init_config", ["fans", "fans_regular", str(percent)])
        if "Loaded" not in resp_str:
            return False

        return True

    def read_fan_speed(self):
        """Read fan speed percantage.

        Args:
            None.

        Returns:
            String representing the fans speed percantage or empty
            string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("read_fan_speed", [])
        return self.__extract_number_from_string(resp_str, 1)

    def get_fan_exist(self, id):
        """Get fan existance status.

        Args:
            id: integer representing the fan id.

        Returns:
            A boolean value, True if fan exist, False if not.
        """
        if not self.is_bmc_fpga_vers_higher_than("2.7.6", "0x30E"):
            return True

        if id in range(1, NUM_FAN_TRAY + 1):
            resp_str = self.__build_and_send_json_rpc("get_fan_exist", [])
            test_str = "FAN {} Exist".format(id)
            val = True if test_str in resp_str else False
        else:
            print("Error: id {} is out of range [1 - {}]".format(id, NUM_FAN_TRAY))
            val = False
        return val

    def get_bmc_version(self):
        """Read BMC version.

        Args:
            None.

        Returns:
            String representing the BMC version or empty string in
            case of error.
        """
        resp_str = self.__build_and_send_json_rpc("get_bmc_version", [])
        return self.__extract_number_from_string(resp_str, 1)

    def get_fpga_version(self):
        """Read FPGA version.

        Args:
            None.

        Returns:
            String representing the FPGA version or empty string in
            case of error.
        """
        resp_str = self.__build_and_send_json_rpc("get_fpga_version", [])
        return self.__extract_number_from_string(resp_str, 1)

    def check_thermal_sensor(self, id):
        """Read the temperature in celsius units of the main board temperature sensor ID.

        Args:
            id: integer representing the temperature sensor id.

        Returns:
            String of integer representing the temperature sample in
            celsius units or empty string in case of error.

        Notes:
            The temperature sensor component can be seen at main board schematic
            component number U68.
            The temperature sensor names are different from the schematic
            and are detailed in the following list:
            Sensor ID       Sensor name             MB temp channel number
            ---------       -----------             ----------------------
            1               Temp_Sensor_Chip        1
            2               Input_Air_Flow          2
            3               Input_OSFP_Air_Flow     3
            4               East_Side_Air_Flow      4
            5               West_Side_Air_Flow      5
            6               Output_1_Air_Flow       6
            7               Output_2_Air_Flow       7
        """
        if id in range(1, NUM_THERMAL_MAIN_BOARD + 1):
            resp_str = self.__build_and_send_json_rpc("check_thermal_sensor", [id])
            val = self.__extract_number_from_string(resp_str, 1)
        else:
            print("Error: id {} is out of range [1 - {}]".format(id, NUM_THERMAL_MAIN_BOARD))
            val = ""
        return val

    def get_cpuboard_sensor(self):
        """Read the temperature in celsius units of the CPU board temperature sensor.

        Args:
            None.

        Returns:
            String of integer representing the temperature sample in
            celsius units or empty string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("get_cpuboard_sensor", [])
        return self.__extract_number_from_string(resp_str, 1)

    def read_x2_thermal(self, id):
        """Read the temperature in celsius units of the chip temperature sensor ID.

        Args:
            id: integer representing the temperature sensor id.

        Returns:
            String of integer representing the temperature sample in
            celsius units or empty string in case of error.

        Notes:
            The sensors names are missing GLC2.
            The temperature sensors are detailed in the following list:
            Sensor ID       Sensor name
            ---------       -----------
            1               GLC0
            2               GLC1
            3               GLC3
        """
        if not self.is_bmc_fpga_vers_higher_than("2.6.9", "0x30E"):
            return ""

        if id in range(1, NUM_THERMAL_CHIP + 1):
            num_idx = [3, 5, 9]
            resp_str = self.__build_and_send_json_rpc("read_x2_thermal", [])
            val = self.__extract_number_from_string(resp_str, num_idx[id-1])
        else:
            print("Error: id {} is out of range [1 - {}]".format(id, NUM_THERMAL_CHIP))
            val = ""
        return val

    def psup_voltage(self):
        """Read PSUP voltage in Volt units.

        Args:
            None.

        Returns:
            String of float number representing PSUP voltage or empty
            string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("psup_voltage", [0])
        return self.__extract_number_from_string(resp_str, 1)

    def power_ctrl_voltage(self, device_id, fpga_client, page):
        """Read voltage in Volt units from PMBus devices.

        Args:
            device_id: integer representing I2C slave address.
            fpga_client: integer representing fpga client (which is act
                as I2C master) of FPGA I2CM_IND block.
            page: integer representing the page number of device's PMBus.

        Returns:
            String of float number representing device's voltage sample
            in Volt units or empty string in case of error.

        Notes:
            1. For valid device_id/fpga_client/page combination please
               refer to the docstring section of the function
               '__is_valid_device_id_combination'
        """
        if not self.__is_valid_device_id_combination(device_id, fpga_client, page):
            return ""

        params = [device_id, fpga_client, page]
        resp_str = self.__build_and_send_json_rpc("power_ctrl_voltage", params)
        return self.__extract_number_from_string(resp_str, 4)

    def psup_power(self):
        """Read PSUP power in Watt units.

        Args:
            None.

        Returns:
            String of float number representing PSUP power or empty
            string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("psup_power", [0])
        return self.__extract_number_from_string(resp_str, 1)

    def get_psup_model(self):
        """Read PSUP P/N model.

        Args:
            None.

        Returns:
            String representing PSUP P/N model or empty string in case of error.
        """
        if not self.is_bmc_fpga_vers_higher_than("2.6.9", "0x30E"):
            return "N/A"

        resp_str = self.__build_and_send_json_rpc("get_psup_model", [])
        return self.__extract_substring_from_string(resp_str, 2, '  ')

    def get_psup_serial_num(self):
        """Read PSUP serial number.

        Args:
            None.

        Returns:
            String representing PSUP serial number or empty string in case of error.
        """
        if not self.is_bmc_fpga_vers_higher_than("2.6.9", "0x30E"):
            return "N/A"

        resp_str = self.__build_and_send_json_rpc("get_psup_serial_num", [])
        return self.__extract_substring_from_string(resp_str, 2, '  ')

    def x2_reset(self, reset):
        """Reset X2 device while CPU is working.

        Args:
            reset: integer representing reset mode.
                0 - assert reset (reset).
                1 - deassert reset (no reset).

        Returns:
            A boolean value, True if the operation succeeded, False if not.
        """
        if reset not in [0, 1]:
            print("Error: reset {} is out of range [0 - 1]".format(reset))
            return False

        resp_str = self.__build_and_send_json_rpc("x2_reset", [reset])
        val = self.__extract_number_from_string(resp_str, 1)
        return True if str(reset) == val else False

    def debug_reset(self, boot_dump):
        """Reset X2 device gracfully while CPU is working.

        Args:
            boot_dump: integer representing boot dump mode.
                0 - do only X2 reset.
                1 - do X2 reset + some operations of autoboot/spiboot/flashboot
                and more operation.
                please see `init_switch` function at the link below for more information:
                https://bbk.xsightlabs.com/projects/XB/repos/vbmc/browse/src/switch.c

        Returns:
            A boolean value, True if the operation succeeded, False if not.

        Notes:
            According to BMC's Confluence, this is useful for quick reset.
        """
        if boot_dump not in [0, 1]:
            print("Error: boot_dump {} is out of range [0 - 1]".format(boot_dump))
            return False

        resp_str = self.__build_and_send_json_rpc("debug_reset", [boot_dump])
        return True if "DONE" in resp_str else False

    def cold_reset(self, type = None):
        """Reset the X2 device with/without the CPU, depending on the input type, in case
        of reset X2 device without CPU, wait for host to issue sudo reboot.

        Args:
            type = list or None representing reset type.
                0    - Reset chip.
                1    - Reset chip and CPU.
                None - Reset chip and CPU (For BMC below 2.7.2 ver)

        Returns:
            A boolean value, True if the operation succeeded, False if not.
        """
        if self.is_bmc_fpga_vers_higher_than("2.7.2", "0x30E"):
            if (type not in [0, 1]):
                print("Error: Invalid type {} for versions above BMC:2.7.2 FPGA:0x30E".format(type))
                return False
            params = [type]
        else:
            if (type != None):
                print("Error: Invalid type {} for versions below BMC:2.7.2 FPGA:0x30E".format(type))
                return False
            params = []

        resp_str = self.__build_and_send_json_rpc("cold_reset", params)
        return True if "DONE" in resp_str else False
