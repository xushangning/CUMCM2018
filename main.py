import world
import rgv
import cnc


def get_event(_):
    return 7


if __name__ == '__main__':
    sim = world.World(get_event, 10000)
    sim.simulate()
