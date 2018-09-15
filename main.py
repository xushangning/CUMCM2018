import world
import rgv
import cnc


def get_event(dic, time):
    if time == 0:
        return 7
    elif time == 40:
        return 8
    elif time == 1000:
        return 7
    elif time == 1100:
        return 9
    elif time == 1800:
        return 7
    elif time == 1900:
        return 9
    elif time == 2000:
        return 8
    elif time == 2050:
        return 9
    elif time == 2100:
        return 4
    elif time == 2200:
        return 7
    elif time == 2800:
        return 7
    elif time == 2900:
        return 9
    elif time == 3000:
        return 8
    elif time == 3900:
        return 8
    elif time == 4000:
        return 9
    else:
        return 0


if __name__ == '__main__':
    sim = world.World(get_event, 10000)
    sim.simulate()
    sim.info()
    sim.final()
