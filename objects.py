from enum import Enum


class Instruction:
    def __init__(self, time: int, action: str, details: list):
        self.time = time
        self.action = action
        self.details = details


class Data(Enum):
    NULL = 0
    ZERO = 1
    ONE = 2


class Cable:
    def __init__(self, device=None, port=None):
        self.device = device
        self.port = port
        self.data = Data.NULL

    def update(self, device, port):
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
        self.remove(self.ports[port])
        port = self.ports[port]
        port.update(other_device, other_port)
        if port.data != Data.NULL:
            self.send_bite(time, port.data)

    def remove(self, port):
        if port.device is None:
            return
        ports_number = port.device.ports_number
        ports = port.device.ports
        for p in range(ports_number):
            if ports[p].device == self:
                ports[p].update(None, None)
                return

    def send_bite(self, time: int, data: Data, disconnected: bool = False):
        self.transmitting_data = data
        for p in range(self.ports_number):
            if self.ports[p] is not None:
                if self.receiving(p):
                    continue
                cable = self.ports[p]
                device = cable.device
                cable.data = data
                if device is None:
                    continue
                string = "time={}, port={}, {}".format(time, p + 1, self.sending())
                if data == data.NULL:
                    self.write("{}null, cause={}\n".format(string,
                                                           self.disconnecting() if disconnected else "data_ended"))
                    if device.ports[cable.port].data != Data.NULL:
                        continue
                else:
                    string = "{}{}, transmission=".format(string, 1 if data == data.ONE else 0)
                    if device.ports[cable.port].data != Data.NULL:
                        self.write("{}collision\n".format(string))
                        continue
                    self.write("{}successfully\n".format(string))
                device.receive_bite(time, cable.port, data, disconnected)
        self.write("\n")

    def receiving(self, port: int):
        return False

    def write(self, string):
        file = open("output/{}.txt".format(self.name), 'a')
        file.write(string)
        file.close()

    def sending(self):
        return "send="

    def disconnecting(self):
        return "disconnected"

    def collision(self, cable):
        cable.data = Data.NULL
        return True

    def receive_bite(self, time: int, port: int, data: Data, disconnected: bool = False):
        self.write("time={}, port={}, receive=".format(time, port + 1))
        if data == Data.NULL:
            self.write("null, cause={}\n".format("host_disconnected" if disconnected else "data_ended"))
        else:
            self.write("{}\n".format(1 if data == data.ONE else 0))

    def disconnect(self, time: int, port: int):
        self.remove(self.ports[port])
        self.ports[port].update(None, None)
