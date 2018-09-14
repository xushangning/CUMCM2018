import world
import rgv
import cnc

if __name__ == '__main__':
    sim = world.World(10000)
    sim.entity_dict['RGV'].inst(rgv.RGV_modecode_rev['supply cargo 1'], 1)
    for i in sim.entity_dict['CNC'][1:]:
        print(i.proc_id, i.proc_clock)
