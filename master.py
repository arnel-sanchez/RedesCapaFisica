from objects import Data
from actions import PhysicalLayer, Instruction, create, connect, send, disconnect


def master(signal_time: int, instructions: list):
    i = 0
    time = 0
    transmitting = []
    ended = []
    physical_layer = PhysicalLayer()
    while i < len(instructions) or len(transmitting) > 0:
        for t in transmitting:
            data = t.send(signal_time, time)
            if data == Data.NULL:
                ended.append(t)
        for t in ended:
            transmitting.remove(t)
        ended.clear()
        if i < len(instructions):
            if len(transmitting) < 1 and time < instructions[i].time:
                time = instructions[i].time
            j = i
            while j < len(instructions) and instructions[j].time == time:
                controller(signal_time, physical_layer, time, instructions[j], transmitting)
                j += 1
            i = j
        time += 1
    return


def controller(signal_time: int, physical_layer: PhysicalLayer, time: int, instruction: Instruction,
               transmitting: list):
    if len(instruction.details) > 3:
        print("\nWRONG INSTRUCTION FORMAT.")
        raise Exception
    if instruction.action == "create":
        create(physical_layer, instruction)
    elif instruction.action == "connect":
        connect(physical_layer, instruction)
    elif instruction.action == "send":
        send(signal_time, physical_layer, instruction, transmitting)
    elif instruction.action == "disconnect":
        disconnect(physical_layer, time, instruction, transmitting)
    else:
        print("\nUNRECOGNIZED INSTRUCTION.")
        raise Exception
    print("{} {}".format(instruction.time, instruction.action), end="")
    for i in range(len(instruction.details)):
        print(" {}".format(instruction.details[i]), end="")
    print()
