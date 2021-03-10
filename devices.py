from objects import Device, Data


class Host(Device):
    def __init__(self, name: str):
        super().__init__(name, 1)
        self.transmitting_started = -1
        self.data = []
        self.data_pointer = 0

    def start_send(self, signal_time, time: int, data: list):
        self.transmitting_started = time
        self.data = data
        self.send(signal_time, time)

    def send(self, signal_time, time):
        if self.transmitting_started == -1 or (time - self.transmitting_started) % signal_time != 0:
            return
        disconnected = len(self.data) < 1
        if self.data_pointer < len(self.data):
            data = Data.ONE if self.data[self.data_pointer] == 1 else Data.ZERO
            self.data_pointer += 1
        else:
            data = Data.NULL
            self.transmitting_started = -1
            self.data = []
            self.data_pointer = 0
        self.send_bite(time, data, disconnected)
        return data

    def receive_bite(self, time: int, port: int, data: Data, disconnected: bool = False):
        super().receive_bite(time, port, data, disconnected)
        self.write("\n")

    def disconnect(self, time: int, port: int):
        self.data = []
        self.send(time, time)
        super().disconnect(time, port)


class Hub(Device):
    def __init__(self, name: str, no_ports: int):
        super().__init__(name, no_ports)
        self.receiving_port = None

    def receiving(self, port: int):
        return port == self.receiving_port

    def sending(self):
        return "resend="

    def disconnecting(self):
        return "host_disconnected"

    def collision(self, cable):
        super().collision(cable)
        if self.receiving_port == cable.port:
            return False
        return True

    def receive_bite(self, time: int, port: int, data: Data, disconnected: bool = False):
        super().receive_bite(time, port, data, disconnected)
        self.receiving_port = port
        self.send_bite(time, data, disconnected)
