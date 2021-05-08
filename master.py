from instructions import Layer, send, Instruction, create, connect, disconnect
from objects import Data


def master(signal_time: int, instructions: list):
    i = 0
    time = 0
    transmitting = []
    ended = []
    layer = Layer(signal_time)
    while i < len(instructions) or len(transmitting) > 0:
        for t in transmitting:
            data = t.send(time)
            if data == Data.NULL:
                ended.append(t)
        for t in ended:
            transmitting.remove(t)
        ended.clear()
        if i < len(instructions):
            if time > instructions[i].time:
                raise Exception
            if len(transmitting) < 1 and time < instructions[i].time:
                time = instructions[i].time
            j = i
            while j < len(instructions) and instructions[j].time == time:
                controller(layer, instructions[j], transmitting)
                j += 1
            i = j
        time += 1
    return time


def controller(layer: Layer, instruction: Instruction, transmitting: list):
    if len(instruction.details) > 3:
        print("\nWRONG INSTRUCTION FORMAT.")
        raise Exception
    if instruction.command == "create":
        create(layer, instruction)
    elif instruction.command == "connect":
        connect(layer, instruction)
    elif instruction.command == "send":
        send(layer, instruction, transmitting)
    elif instruction.command == "disconnect":
        disconnect(layer, instruction)
    else:
        print("\nUNRECOGNIZED INSTRUCTION.")
        raise Exception
    print("{} {}".format(instruction.time, instruction.command), end="")
    for i in range(len(instruction.details)):
        print(" {}".format(instruction.details[i]), end="")
    print()
