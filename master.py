from actions import PhysicalLayer, controller


def master(signal_time: int, principal: list):
    i = 0
    time = 0
    transmitting = []
    current = []

    physical_layer = PhysicalLayer()

    while i < len(principal):
        if time < principal[i].time:
            time = principal[i].time
        j = i
        while j < len(principal) and principal[j].time <= time:
            controller(physical_layer, principal[j], transmitting)

            current.append(principal[j])
            j += 1

        i = j



