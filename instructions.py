from layer import Layer
from objects import Instruction


def create(layer: Layer, instruction: Instruction):
    device = instruction.details[0]
    name = instruction.details[1]
    if device == "hub":
        ports_number = int(instruction.details[2])
        if ports_number < 1:
            print("\nWRONG PORTS NUMBER.")
            raise Exception
    elif device == "host":
        if len(instruction.details) > 2:
            print("\nWRONG CREATE HOST INSTRUCTION FORMAT.")
            raise Exception
        ports_number = 1
    else:
        print("\nUNRECOGNIZED DEVICE TYPE.")
        raise Exception
    layer.create(device, name, ports_number)
    write(instruction.time, "create, device={}, name={}{}\n".format(device, name, ", ports_number={}".
                                                                    format(ports_number)
                                                                    if device == ("hub" or "switch") else ""))


def write(time: int, string: str):
    file = open("output/general.bin", 'a')
    file.write("time={}, instruction={}".format(time, string))
    file.close()


def connect(layer: Layer, instruction: Instruction):
    if len(instruction.details) > 2:
        print("\nWRONG CONNECT INSTRUCTION FORMAT.")
        raise Exception
    port1 = str.split(instruction.details[0], '_')
    port2 = str.split(instruction.details[1], '_')
    layer.connect(instruction.time, port1[0], int(port1[1]) - 1, port2[0], int(port2[1]) - 1)
    write(instruction.time, "connect, device_x={}, port_x={}, device_y={}, port_y={}\n".format(port1[0], port1[1],
                                                                                               port2[0], port1[1]))


def send(signal_time: int, layer: Layer, instruction: Instruction, transmitting: list):
    if len(instruction.details) > 2:
        print("\nWRONG SEND INSTRUCTION FORMAT.")
        raise Exception
    host = instruction.details[0]
    details = instruction.details[1]
    data = [int(details[i]) for i in range(len(details))]
    for i in range(len(data)):
        if data[i] != 0 and data[i] != 1:
            print("\nUNRECOGNIZED DATA TYPE.")
            raise Exception
    device = layer.send(signal_time, instruction.time, host, data)
    if device is not None:
        transmitting.append(device)
    write(instruction.time, "send, host={}, data={}\n".format(host, details))


def disconnect(layer: Layer, instruction: Instruction):
    if len(instruction.details) > 1:
        print("\nWRONG DISCONNECT INSTRUCTION FORMAT.")
        raise Exception
    port = str.split(instruction.details[0], '_')
    layer.disconnect(instruction.time, port[0], int(port[1]) - 1)
    write(instruction.time, "disconnect, device={}, port={}\n".format(port[0], port[1]))
