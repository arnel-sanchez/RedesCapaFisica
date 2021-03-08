from objects import Hub, Host, Cable, Device, Data


class PhysicalLayer:
    def __init__(self):
        self.devices = set()

    def create(self, device: str, name: str, ports_no: int = 1):
        if device == "hub":
            self.devices.add(Hub(name, ports_no))
        elif device == "host":
            self.devices.add(Host(name))

    def connect(self, device1: str, port1: int, device2: str, port2: int):
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
        if port1 > d1.ports_no or port2 > d2.ports_no:
            print("\nUNRECOGNIZED PORT.")
            raise Exception
        d1.connect(d2, port1)
        d2.connect(d1, port2)
        # Empezar a recibir/enviar en caso de que uno de los dos este transmitiendo

    def send(self, host: str, data):
        for d in self.devices:
            if d.name == host:
                if type(d) != Host:
                    print("\nWRONG SEND INSTRUCTION DEVICE TYPE.")
                    raise Exception
                d.data = data
                self.send_bite(d, Data.NULL)
                return
        print("\nUNRECOGNIZED DEVICE.")
        raise Exception

    def send_bite(self, device: Device, data: Data):
        if type(data) != Data:
            raise Exception
        port = device.ports[0]
        if port.data != Data.NULL and data != Data.NULL:
            return False
        port.data = data
        self.resend(port.device, data)
        return True

    def resend(self, device, data):
        if type(device) != Hub:
            return
        ports = device.ports
        for p in ports:
            if p is not None:
                p.data = data
                other_device = p.device
                self.resend(other_device, data)

    def disconnect(self, device: str, port: int):
        for d in self.devices:
            if d.name == device:
                if port > d.ports_no:
                    print("\nUNRECOGNIZED PORT.")
                    raise Exception
                if d.ports[0].data != Data.NULL:
                    self.end_send(d)
                d.disconnect(port)
                # Empezar a recibir/enviar en caso de que este transmitiendo
                return
        print("\nUNRECOGNIZED DEVICE.")
        raise Exception

    def end_send(self, host):
        self.send_bite(host, Data.NULL)
