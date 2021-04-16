from os import mkdir, listdir, remove, path
from master import master, Instruction


def main():
    if not directory():
        return
    try:
        script = open("input/script.txt", 'r')
    except OSError:
        print("\nSCRIPT WAS NOT FOUND.\n")
        return
    signal_time = 10
    try:
        config = open("input/config.txt", 'r')
    except OSError:
        print("\nCONFIG WAS NOT FOUND.\n")
    else:
        try:
            while True:
                line = config.readline().replace(' ', '')
                if len(line) < 1:
                    break
                line = line.split('=')
                if line[0] == "signal_time":
                    signal_time = int(line[1])
                else:
                    raise Exception
        except Exception:
            print("\nCONFIG FORMAT ERROR.\n")
            signal_time = 10
    try:  # Comment to debug
        print("\nCONNECTION STARTED.")
        print("(TIME = 0)\n")
        time = master(signal_time, translator(script))
        script.close()
        print("\nCONNECTION ENDED.")
        print("(TIME = {})\n".format(time))
    except Exception:
        print("\nBAD FORMAT ERROR.\n")


def directory():
    try:
        mkdir("output")
    except OSError:
        print("\nOUTPUT DIRECTORY CREATION FAILED.")
        try:
            for file in listdir("output"):
                remove(path.join("output", file))
        except OSError:
            print("\nOUTPUT DIRECTORY CLEANING FAILED.")
            return False
    file = open("output/general.bin", 'w')
    file.close()
    return True


def translator(script):
    instructions = []
    while True:
        line = script.readline()
        line = line.replace('\n', '')
        if len(line) < 1:
            break
        line = line.split(' ')
        instructions.append(Instruction(int(line[0]), line[1], line[2:len(line)]))
    return instructions


if __name__ == '__main__':
    main()
