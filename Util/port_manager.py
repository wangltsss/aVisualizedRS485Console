import serial

import serial.tools.list_ports

import platform

from time import sleep

from Util.json_parser import Parser


board_conf_path = "conf/board.json"


class PortManager(object):

    _system = platform.system()
    _jsonParser = Parser()

    ser: serial.Serial
    _serial_port: str

    def set_port(self, port):
        self._serial_port = port

    def get_port(self):
        return self._serial_port

    def list_ports(self):
        list_p = list(serial.tools.list_ports.comports())
        list_ports_name = []
        if self._system.lower() == "darwin":
            list_ports_name = [str(i.name) for i in list_p]
        elif self._system.lower() == "windows":
            list_ports_name = [str(i.device) for i in list_p]
        return list_ports_name

    def create_connection(self, port):
        res = self._jsonParser.json_reader(board_conf_path)
        if self._system.lower() == "darwin":
            self.ser = serial.Serial(port="/dev/{}".format(port),
                                     baudrate=res["baudrate"],
                                     bytesize=res["bytesize"],
                                     stopbits=res["stopbits"])
        elif self._system.lower() == "windows":
            self.ser = serial.Serial(port=port,
                                     baudrate=res["baudrate"],
                                     bytesize=res["bytesize"],
                                     stopbits=res["stopbits"])

    def send_data(self, value):
        print("send_data is executed")
        write_data = bytearray.fromhex(value)
        print(write_data)
        sleep(0.3)
        try:
            self.ser.write(write_data)
            print(str(write_data) + " has been sent.")
            return True
        except Exception as e:
            print(e)
            return False

    def read_data(self):
        print("read_data is executed")
        try:
            sleep(0.3)
            if self.ser.inWaiting():
                bs = self.ser.read(self.ser.inWaiting()).hex()
                res = ''
                for i in range(len(bs)):
                    res += bs[i]
                    if i % 2 == 1:
                        res += ' '
                res = res.rstrip(' ')
                return res
            else:
                return ""
        except Exception as e:
            print(e)
            return None

    def close(self, ser):
        ser.close()
















