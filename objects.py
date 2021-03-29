from enum import Enum


class Instruction:
    def __init__(self, time: int, command: str, details: list):
        self.time = time
        self.command = command
        self.details = details


class Data(Enum):
    NULL = 0
    ZERO = 1
    ONE = 2


class Cable:
    def __init__(self, device=None, port: int = -1):
        self.device = device
        self.port = port
        self.data = Data.NULL

    def update(self, device=None, port: int = -1):
        self.device = device
        self.port = port
