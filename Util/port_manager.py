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
                                     stopbits=1,
                                     timeout=0.5
                                     )
        elif self._system.lower() == "windows":
            self.ser = serial.Serial(port=port,
                                     baudrate=115200,
                                     bytesize=8,
                                     stopbits=1,
                                     timeout=0.5)

    def send_data(self, value):
        write_data = bytearray.fromhex(value)
        try:
            sleep(0.1)
            if self.ser.out_waiting:
                self.ser.reset_output_buffer()
            if self.ser.write(write_data):
                self.ser.flush()
            else:
                if self.ser.write(write_data):
                    self.ser.flush()
            self.ser.reset_output_buffer()
            return True
        except Exception as e:
            print(e)
            self.ser.reset_output_buffer()
            return False

    def read_data(self):
        try:
            i = 0
            while i < 2:
                sleep(0.1)
                i += 1
                if self.ser.in_waiting:
                    bs = self.ser.read(self.ser.in_waiting).hex()
                    self.ser.reset_input_buffer()
                    res = ''
                    for i in range(len(bs)):
                        res += bs[i]
                        if i % 2 == 1:
                            res += ' '
                    res = res.rstrip(' ')
                    return res
            self.ser.reset_input_buffer()
            return ""
        except Exception as e:
            print(e)
            self.ser.reset_input_buffer()
            return None

    def close(self, *ser):
        if ser:
            ser[0].close()
        else:
            self.ser.close()

















