# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 Xsightlabs Ltd.

import subprocess
import socket
import json
import re
import os

# Notes
# 1. The main board schematic version refered in this file is REV. 1
# 2. The cpu board schematic version refered in this file is REV. 1

MAIN_BOARD_THERMAL_SENSOR_NAMES = [
    "Chip Diode",
    "Input Air",
    "OSFP",
    "East Side",
    "West Side",
    "Output Air 1",
    "Output Air 2"
]

CPU_BOARD_THERMAL_SENSOR_NAMES = [
    "CPU Board"
]

ASIC_THERMAL_SENSOR_NAMES = [
    "GLC0",
    "GLC1",
    "GLC3"
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
            self.sock.connect((hostname, port))
        except:
            print("Error: Failed to connect to socket")

    def __del__(self):
        """Close socket connection.

        Args:
            None.

        Returns:
            None.
        """
        self.sock.close()

    def __extract_number_from_string(self, input_str, num_idx):
        """Get a number (integer, float, hex) from a list of number string,
        which is extracted from the input string.

        Args:
            input_str: input string.
            num_idx: integer representing the index of number in the string
                to return.

        Returns:
            String representing the number that has been extracted from
            the input string, or empty string in case of error.
        """
        ret_str = ""
        reg_pattern = r"0[xX][0-9a-fA-F]+|\d+.\d+.\d+|[-+]?\d*\.?\d+|[-+]?\d+"
        num_list = re.findall(reg_pattern, input_str)
        if len(num_list) >= num_idx:
            ret_str = num_list[num_idx - 1]
        else:
            print("Error: Failure in expected list length ", len(num_list))
        return ret_str

    def __extract_string_from_string(self, input_str, num_idx, delim):
        ret_str = ""
        jsonobj = json.loads(input_str)
        str_list_= (jsonobj['result']).split(delim)
        if len(str_list_) >= num_idx:
            ret_str = str_list_[num_idx - 1]
        else:
            print("Error: Failure in expected list length ", len(str_list_))
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
        except:
            print("Error: Failed to send message over socket")
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
        if (not(0 <= current_type <= 2)):
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

    def sys_led_ctrl(self, red, green, blue):
        """Set system led RGB (Red, Green, Blue) colors.

        Args:
            red: integer of 0/1.
            green: integer of 0/1.
            blue: integer of 0/1.

        Returns:
            None.

        Notes:
            The system led color is selected in FPGA registers at:
            http://soc.xsight.ent/app/viewItem.cgi?itm=reg&p=1020&b=2&&r=27&
        """
        if (0 <= red <= 1) and (0 <= green <= 1) and (0 <= blue <= 1):
            params = [red, green, blue]
            self.__build_and_send_json_rpc("sys_led_ctrl", params)
        else:
            print("Error: RGB [{},{},{}] is out of range [0 - 1]".format(
                red, green, blue))

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
            self.sys_led_ctrl(red, green, blue)
        else:
            print("Error: color {} is out of range [0 - 3]".format(color))

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
            None.

        Notes:
            This function changed the fan speed both in run time and in BMC's
            configuration file to keep the changes after BMC reboot.
            The BMC has a method to set the fan speed in runtime to both `regular`
            and `hot` modes, when we use this method the fan speed for `hot` mode
            is always to 100%.
        """
        if 0 <= percent <= 100:
            self.__build_and_send_json_rpc("set_default_fan_values", [percent, 100])
            self.__build_and_send_json_rpc("init_config", ["fans", "fans_regular", str(percent)])
        else:
            print("Error: percent {} is out of range [0 - 100]".format(percent))

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
        """Read temperature sensor sample in celsius units for input sensor ID.

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
        if 1 <= id <= 7:
            resp_str = self.__build_and_send_json_rpc("check_thermal_sensor", [id])
            val = self.__extract_number_from_string(resp_str, 1)
        else:
            print("Error: id {} is out of range [1 - 7]".format(id))
            val = ""
        return val

    def get_cpuboard_sensor(self):
        """Read cpuboard temperature sensor sample in celsius units.

        Args:
            None.

        Returns:
            String of integer representing the temperature sample in
            celsius units or empty string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("get_cpuboard_sensor", [])
        return self.__extract_number_from_string(resp_str, 1)

    def read_x2_thermal(self, id):
        """Read chip temperature sensor id sample in celsius units.

        Args:
            None.

        Returns:
            String of integer representing the temperature sample in
            celsius units or empty string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("read_x2_thermal", [])
        if id == 1:
            num_idx = 3
        elif id == 2:
            num_idx = 5
        elif id == 3:
            num_idx = 9
        else:
            num_idx = 3
        return self.__extract_number_from_string(resp_str, num_idx)

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
            String of float number representing PSUP P/N model or empty
            string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("get_psup_model", [])
        return self.__extract_string_from_string(resp_str, 2, '  ')

    def get_psup_serial_num(self):
        """Read PSUP serial number.

        Args:
            None.

        Returns:
            String of float number representing PSUP serial number or empty
            string in case of error.
        """
        resp_str = self.__build_and_send_json_rpc("get_psup_serial_num", [])
        return self.__extract_string_from_string(resp_str, 2, '  ')

    def x2_reset(self, reset):
        """Reset X2 device while CPU is working.

        Args:
            reset: integer representing reset mode.
                0 - assert reset (reset).
                1 - deassert reset (no reset).

        Returns:
            None.
        """
        if 0 <= reset <= 1:
            self.__build_and_send_json_rpc("x2_reset", [reset])
        else:
            print("Error: reset {} is out of range [0 - 1]".format(reset))

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
            None.

        Notes:
            According to BMC's Confluence, this is useful for quick reset.
        """
        if 0 <= boot_dump <= 1:
            self.__build_and_send_json_rpc("debug_reset", [boot_dump])
        else:
            print("Error: boot_dump {} is out of range [0 - 1]".format(boot_dump))

    def cold_reset(self):
        """Reset X2 device and CPU during normal operation.

        Args:
            None.

        Returns:
            None.
        """
        self.__build_and_send_json_rpc("cold_reset", [])
