from host import Hub, Host


class Layer:
    def __init__(self):
        self.devices = set()

    def create(self, device: str, name: str, ports_number: int = 1):
        if device == "hub":
            self.devices.add(Hub(name, ports_number))
        elif device == "host":
            self.devices.add(Host(name))

    def connect(self, time: int, device1: str, port1: int, device2: str, port2: int):
        if device1 == device2:
            print("\nCAN'T CONNECT A DEVICE WITH ITSELF.")
            raise Exception
        d1 = None
        d2 = None
        for d in self.devices:
            if d.name == device1:
                d1 = d
            elif d.name == device2:
                d2 = d
        if d1 is None or d2 is None:
            print("\nUNRECOGNIZED DEVICE.")
            raise Exception
        if port1 > d1.ports_number or port2 > d2.ports_number:
            print("\nUNRECOGNIZED PORT.")
            raise Exception
        d1.connect(time, port1, d2, port2)
        d2.connect(time, port2, d1, port1)

    def send(self, signal_time: int, time: int, host: str, data: list):
        for d in self.devices:
            if d.name == host:
                if type(d) != Host:
                    print("\nWRONG SEND INSTRUCTION DEVICE TYPE.")
                    raise Exception
                new = d.start_send(signal_time, time, data)
                return d if new else None
        print("\nUNRECOGNIZED DEVICE.")
        raise Exception

    def disconnect(self, time: int, device: str, port: int):
        for d in self.devices:
            if d.name == device:
                if port > d.ports_number:
                    print("\nUNRECOGNIZED PORT.")
                    raise Exception
                d.disconnect(time, port)
                return
        print("\nUNRECOGNIZED DEVICE.")
        raise Exception
