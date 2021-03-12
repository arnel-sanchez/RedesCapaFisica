from enum import Enum


class Instruction:
    def __init__(self, time: int, command: str, details: list):
        self.time = time
        self.command = command
        self.details = details


class Data(Enum):
    NULL = 0
    ZERO = 1
    ONE = 2


class Cable:
    def __init__(self, device=None, port: int = -1):
        self.device = device
        self.port = port
        self.data = Data.NULL

    def update(self, device=None, port: int = -1):
        self.device = device
        self.port = port


class Device:
    def __init__(self, name: str, ports_number: int):
        self.name = name
        self.ports_number = ports_number
        self.ports = [Cable() for _ in range(ports_number)]
        self.transmitting_data = Data.NULL
        file = open("output/{}.txt".format(name), 'w')
        file.close()

    def connect(self, time: int, port: int, other_device, other_port: int):
        cable = self.ports[port]
        device = cable.device
        if device is not None:
            device.disconnect(time, cable.port)
        cable.update(other_device, other_port)
        data = cable.data
        if data != Data.NULL:
            string = "time={}, port={}, send={}, transmission=".format(time, port + 1, 1 if data == data.ONE else 0)
            if other_device.transmitting_data != Data.NULL:
                self.collision(other_device, string)
                self.write("\n")
            else:
                self.write("{}successfully\n\n".format(string))
                other_device.receive_bit(time, other_port, data)

    def disconnect(self, time: int, port: int):
        cable = self.ports[port]
        device = cable.device
        cable.update()
        if device is None:
            return
        ports_number = device.ports_number
        ports = device.ports
        for p in range(ports_number):
            if ports[p].device == self:
                device.disconnect(time, p)
                return

    def collision(self, device, string: str):
        self.write("{}collision\n".format(string))

    def write(self, string: str):
        file = open("output/{}.txt".format(self.name), 'a')
        file.write(string)
        file.close()

    def receive_bit(self, time: int, port: int, data: Data, disconnected: bool = False):
        self.write("time={}, port={}, receive=".format(time, port + 1))
        if data == Data.NULL:
            self.write("null, cause={}\n".format("host_disconnected" if disconnected else "data_ended"))
        else:
            self.write("{}\n".format(1 if data == data.ONE else 0))

    def send_bit(self, time: int, data: Data, disconnected: bool = False):
        self.transmitting_data = data
        new_line = False
        for p in range(self.ports_number):
            if self.receiving(p):
                continue
            string = "time={}, port={}, {}".format(time, p + 1, self.sending())
            cable = self.ports[p]
            cable.data = data
            device = cable.device
            if device is None:
                if not disconnected:
                    self.write("{}{}, transmission=incomplete, cause=not_connected\n".format(string,
                                                                                             1 if data == data.ONE
                                                                                             else 0 if data == data.ZERO
                                                                                             else
                                                                                             "null, cause=data_ended"))
                    new_line = True
            else:
                port = cable.port
                if data == data.NULL:
                    if not disconnected:
                        self.write("{}null, cause=data_ended\n".format(string))
                        new_line = True
                    if device.ports[port].data != Data.NULL:
                        continue
                else:
                    string = "{}{}, transmission=".format(string, 1 if data == data.ONE else 0)
                    new_line = True
                    if device.ports[port].data != Data.NULL:
                        self.collision(device, string)
                        continue
                    self.write("{}successfully\n".format(string))
                device.receive_bit(time, port, data, disconnected)
        if new_line:
            self.write("\n")

    def receiving(self, port: int):
        return False

    def sending(self):
        return "send="
