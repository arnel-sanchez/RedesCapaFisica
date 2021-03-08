from os import rmdir, mkdir
from objects import Instruction
from master import master


def main():
    if not directory():
        return
    try:
        script = open("script.txt", 'r')
    except OSError:
        print("\nSCRIPT WAS NOT FOUND.\n")
        return
    signal_time = 10
    try:
        print("\nCONNECTION STARTED.\n")
        master(signal_time, translator(script))
        print("\nCONNECTION ENDED.\n")
    except Exception:
        print("\nBAD FORMAT ERROR.\n")


def directory():
    try:
        rmdir("output")
    except OSError:
        print("\nOUTPUT DIRECTORY DELETION FAILED.\n")
    try:
        mkdir("output")
    except OSError:
        print("\nOUTPUT DIRECTORY CREATION FAILED.\n")
        return False
    return True


def translator(script):
    instructions = []
    while True:
        line = script.readline()
        if line == '':
            break
        line = line.replace('\n', '').split(' ')
        instructions.append(Instruction(int(line[0]), line[1], line[2:len(line)]))
    return instructions


if __name__ == '__main__':
    main()
