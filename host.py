from hub import Device, Data, Hub


class Host(Device):
    def __init__(self, name: str):
        super().__init__(name, 1)
        self.transmitting_started = -1
        self.data = []
        self.data_pointer = 0
        self.resend_attempts = 0

    def disconnect(self, time: int, port: int):
        cable = self.ports[port]
        device = cable.device
        if device is None:
            return
        if len(self.data) > 0:
            device.receive_bit(time, cable.port, Data.NULL, True)
        if type(device) == Hub and device.ports[cable.port].data != Data.NULL:
            self.receive_bit(time, cable.port, Data.NULL, True)
        super().disconnect(time, port)
        self.data_pointer = 0  # Comment if the the host must not restart sending data in case of disconnection

    def receive_bit(self, time: int, port: int, data: Data, disconnected: bool = False):
        super().receive_bit(time, port, data, disconnected)
        self.write("\n")

    def collision(self, device, string: str):
        super().collision(device, string)
        if self.data_pointer > 0:
            self.data_pointer -= 1  # Comment if the the host must not wait to resend data in case of collision
        self.resend_attempts += 1
        if self.resend_attempts == 20:
            self.reset()
        if type(device) == Host and device.transmitting_started <= self.transmitting_started:
            self.ports[0].data = Data.NULL

    def reset(self):
        self.transmitting_started = -1
        self.data = []
        self.data_pointer = 0
        self.resend_attempts = 0

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
            self.reset()
        self.send_bit(time, data, disconnected)
        if self.ports[0].device is None:
            self.data_pointer -= 1  # Comment if the the host must not wait to resend data in case of disconnection
            self.resend_attempts += 1
            if self.resend_attempts == 20:
                self.reset()
        else:
            self.resend_attempts = 0
        return data if not disconnected else data.ZERO
