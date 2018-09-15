import world
import rgv
import cnc


def get_event(dic, time):
    if time == 0:
        return 7
    elif time == 1000:
        return 7
    elif time == 1100:
        return 8
    elif time == 1800:
        return 8
    elif time == 2000:
        return 9
    elif time == 2100:
        return 4
    elif time == 2200:
        return 7
    else:
        return 0


if __name__ == '__main__':
    t = [1, 2, 2, 2, 2, 2, 2, 2]
    sim = world.World(get_event, t, 3600 * 8)
    sim.simulate()
    sim.info()
    sim.final()
