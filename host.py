from hub import Device, Data


class Host(Device):
    def __init__(self, name: str):
        super().__init__(name, 1)
        self.transmitting_started = -1
        self.data = []
        self.data_pointer = [0, 0]
        self.resend_attempts = 0

    def disconnect(self, time: int, port: int):
        cable = self.ports[port]
        device = cable.device
        if device is None:
            return
        if len(self.data) > 0:
            device.receive_bit(time, cable.port, Data.NULL, True)
        if type(device) != Host and device.ports[cable.port].data != Data.NULL:
            self.receive_bit(time, cable.port, Data.NULL, True)
        super().disconnect(time, port)
        self.data_pointer[1] = 0  # Comment if the the host must not restart sending data in case of disconnection

    def collision(self, device, string: str):
        super().collision(device, string)
        if self.data_pointer[1] > 0:  # Comment if the the host must not wait to resend data in case of collision
            self.data_pointer[1] -= 1
        self.resend_attempts += 1
        if self.resend_attempts == 20:
            self.reset()
        if type(device) == Host and device.transmitting_started <= self.transmitting_started:
            self.ports[0].data = Data.NULL

    def reset(self):
        self.transmitting_started = -1
        self.data = []
        self.data_pointer = [0, 0]
        self.resend_attempts = 0
        self.ports[0].data = Data.NULL

    def receive_bit(self, time: int, port: int, data: Data, disconnected: bool = False):
        super().receive_bit(time, port, data, disconnected)
        self.write("\n")

    def start_send(self, signal_time: int, time: int, data: list):
        self.data.append(data)
        if len(self.data) == 1:
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
        else:
            current = self.data_pointer[0]
            pointer = self.data_pointer[1]
            if pointer < len(self.data[current]):
                data = Data.ONE if self.data[current][pointer] == 1 else Data.ZERO
                self.data_pointer[1] += 1
            else:
                self.data_pointer[0] += 1
                self.data_pointer[1] = 0
                current += 1
                if current < len(self.data):
                    data = Data.ONE if self.data[current][0] == 1 else Data.ZERO
                else:
                    data = Data.NULL
                    self.reset()
        self.send_bit(time, data, disconnected)
        if self.ports[0].device is None:
            self.data_pointer[1] -= 1  # Comment if the the host must not wait to resend data in case of disconnection
            self.resend_attempts += 1
            if self.resend_attempts == 20:
                self.reset()
        else:
            self.resend_attempts = 0
        return data if not disconnected and len(self.data) < 1 else data.ZERO
