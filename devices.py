from objects import Device, Data


class Host(Device):
    def __init__(self, name: str):
        super().__init__(name, 1)
        self.transmitting_started = -1
        self.data = []
        self.data_pointer = 0

    def disconnect(self, time: int, port: int):
        device = self.ports[port].device
        if device is None:
            return
        device.receive_bit(time, port, Data.NULL, True)
        super().disconnect(time, port)

    def receive_bit(self, time: int, port: int, data: Data, disconnected: bool = False):
        super().receive_bit(time, port, data, disconnected)
        self.write("\n")

    def collision(self, device, string: str):
        super().collision(device, string)
        self.data_pointer -= 1  # Comment if the the host must not wait to resend data in case of collision
        if type(device) == Host and device.transmitting_started <= self.transmitting_started:
            self.ports[0].data = Data.NULL

    def start_send(self, signal_time: int, time: int, data: list):
        count = len(self.data)
        for d in data:
            self.data.append(d)
        if count < 1:
            self.transmitting_started = time
            self.send(signal_time, time)
            return True
        return False

    def send(self, signal_time: int, time: int, disconnected: bool = False):
        if self.transmitting_started == -1:
            return Data.NULL
        if (time - self.transmitting_started) % signal_time != 0:
            return Data.ZERO
        if disconnected:
            data = Data.NULL
        elif self.data_pointer < len(self.data):
            data = Data.ONE if self.data[self.data_pointer] == 1 else Data.ZERO
            self.data_pointer += 1
        else:
            data = Data.NULL
            self.transmitting_started = -1
            self.data = []
            self.data_pointer = 0
        self.send_bit(time, data, disconnected)
        if self.ports[0].device is None:
            self.data_pointer -= 1
            # Comment after the "or" if the the host must not wait to resend data in case of disconnection
        return data if not disconnected else data.ZERO


class Hub(Device):
    def __init__(self, name: str, no_ports: int):
        super().__init__(name, no_ports)
        self.receiving_port = None

    def disconnect(self, time: int, port: int):
        if self.receiving_port == port and type(self.ports[port].device) == Hub:
            self.receive_bit(time, port, Data.NULL, True)
        super().disconnect(time, port)

    def receive_bit(self, time: int, port: int, data: Data, disconnected: bool = False):
        super().receive_bit(time, port, data, disconnected)
        if disconnected:
            self.write("\n")
        self.receiving_port = port
        self.send_bit(time, data, disconnected)

    def receiving(self, port: int):
        return self.receiving_port == port

    def sending(self):
        return "resend="
