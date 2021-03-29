from device import Device
from objects import Data


class Hub(Device):
    def __init__(self, name: str, no_ports: int):
        super().__init__(name, no_ports)
        self.receiving_port = -1

    def disconnect(self, time: int, port: int):
        if self.receiving_port == port and type(self.ports[port].device) == Hub:
            self.receive_bit(time, port, Data.NULL, True)
        super().disconnect(time, port)

    def receive_bit(self, time: int, port: int, data: Data, disconnected: bool = False):
        if data == Data.NULL and self.transmitting_data == data.NULL:
            return
        self.receiving_port = port
        new_line = False
        for p in range(self.ports_number):
            if self.receiving_port == p and (data != Data.NULL or self.transmitting_data != data.NULL):
                super().receive_bit(time, p, data, disconnected)
                new_line = True
                break
        if disconnected and new_line:
            self.write("\n")
        self.send_bit(time, data, disconnected)

    def receiving(self, port: int):
        return self.receiving_port == port

    def sending(self):
        return "resend="
