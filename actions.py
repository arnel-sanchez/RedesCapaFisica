from objects import Instruction
from physical_layer import PhysicalLayer


def controller(physical_layer: PhysicalLayer, instruction: Instruction, transmitting: list):
    if len(instruction.details) > 3:
        print("\nWRONG INSTRUCTION FORMAT.")
        raise Exception
    if instruction.action == "create":
        create(physical_layer, instruction)
    elif instruction.action == "connect":
        connect(physical_layer, instruction)
    elif instruction.action == "send":
        send(physical_layer, instruction, transmitting)
    elif instruction.action == "disconnect":
        disconnect(physical_layer, instruction, transmitting)
    else:
        print("\nUNRECOGNIZED COMMAND.")
        raise Exception

    print(str(instruction.time) + " " + instruction.action, end="")
    for i in range(len(instruction.details)):
        print(" " + instruction.details[i], end="")
    print()


def create(physical_layer: PhysicalLayer, instruction: Instruction):
    device = instruction.details[0]
    name = instruction.details[1]
    if device == "hub":
        ports_no = int(instruction.details[2])
        if ports_no < 1:
            print("\nWRONG PORTS NUMBER.")
            raise Exception
    elif device == "host":
        if len(instruction.details) > 2:
            print("\nWRONG CREATE HOST INSTRUCTION FORMAT.")
            raise Exception
        ports_no = 1
    else:
        print("\nUNRECOGNIZED DEVICE TYPE.")
        raise Exception
    physical_layer.create(device, name, ports_no)


def connect(physical_layer: PhysicalLayer, instruction: Instruction):
    if len(instruction.details) > 2:
        print("\nWRONG CONNECT INSTRUCTION FORMAT.")
        raise Exception
    port1 = str.split(instruction.details[0], '_')
    port2 = str.split(instruction.details[1], '_')
    physical_layer.connect(port1[0], int(port1[1]) - 1, port2[0], int(port2[1]) - 1)


def send(physical_layer: PhysicalLayer, instruction: Instruction, transmitting: list):
    if len(instruction.details) > 2:
        print("\nWRONG SEND INSTRUCTION FORMAT.")
        raise Exception
    host = instruction.details[0]
    data = list(instruction.details[1])

    for i in range(len(data)):
        if data[i] != '0' and data[i] != '1':
            print("\nUNRECOGNIZED DATA TYPE.")
            raise Exception
        data[i] = int(data[i])

    if physical_layer.send(host, data):
        transmitting.append(host)


def disconnect(physical_layer: PhysicalLayer, instruction: Instruction, transmitting: list):
    if len(instruction.details) > 1:
        print("\nWRONG DISCONNECT INSTRUCTION FORMAT.")
        raise Exception
    port = str.split(instruction.details[0], '_')
    physical_layer.disconnect(port[0], int(port[1]) - 1)

    hosts = []
    for t in transmitting:
        if t == port[0]:
            hosts.append(t)
    for h in hosts:
        transmitting.remove(h)
