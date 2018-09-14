import world
import rgv
import cnc


def get_event(dic, time):
    if time == 0:
        return 7
    elif time == 1000:
        return 8
    else:
        return 0


if __name__ == '__main__':
    sim = world.World(get_event, 10000)
    sim.simulate()
    sim.final()
