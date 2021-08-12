import serial

import serial.tools.list_ports

import platform

from time import sleep


class PortManager(object):

    _system = platform.system()

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
        if self._system.lower() == "darwin":
            self.ser = serial.Serial(port="/dev/{}".format(port),
                                     baudrate=115200,
                                     bytesize=8,
                                     stopbits=1)
        elif self._system.lower() == "windows":
            self.ser = serial.Serial(port=port,
                                     baudrate=115200,
                                     bytesize=8,
                                     stopbits=1)

    def send_data(self, value):
        write_data = bytearray.fromhex(value)
        try:
            sleep(0.1)
            self.ser.write(write_data)
            return True
        except Exception as e:
            print(e)
            return False

    def read_data(self):
        try:
            sleep(0.1)
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
















