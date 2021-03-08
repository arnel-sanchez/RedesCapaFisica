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
        self.data = Data.NULL


class Device:
    def __init__(self, name: str, ports_no: int):
        self.name = name
        self.ports_no = ports_no
        self.ports = [Cable()] * ports_no
        self.transmitting_data = Data.NULL

    def connect(self, port: int, other_device, other_port: int):
        self.remove(self.ports[port])
        self.ports[port].update(other_device, other_port)

    def remove(self, port):
        if port.device is None:
            return
        ports_no = port.device.ports_no
        ports = port.device.ports
        for p in range(ports_no):
            if ports[p] == self:
                ports[p].update(None, None)

    def disconnect(self, port: int):
        self.remove(self.ports[port])
        self.ports[port].update(None, None)

    def send_bite(self, data: Data):
        # Analizar prioridades en caso de colision
        for p in range(self.ports_no):
            if self.ports[p] is not None:
                self.ports[p].data = data


class Host(Device):
    def __init__(self, name: str):
        super().__init__(name, 1)
        self.data = []
        self.data_pointer = 0

    def send(self):
        if len(self.data) < 1:
            data = Data.NULL
        else:
            data = Data.ONE if self.data[self.data_pointer] == 1 else Data.ZERO
            self.data_pointer += 1
            if self.data_pointer == len(self.data):
                self.data = []
                self.data_pointer = 0
        # Analizar prioridades en caso de colision
        self.send_bite(data)


class Hub(Device):
    def __init__(self, name: str, no_ports: int):
        super().__init__(name, no_ports)
        self.receiving_port = None
