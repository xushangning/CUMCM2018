import numpy as np

import cnc
import rgv
import world


def decode(chromosome):
    """
    Decode chromosome to generate a schedule.

    :param chromosome:
    :return:
    """
    def alg(entity_dict, clock):
        target_cnc = alg.chromosome[alg.index]
        # if RGV is right in front of the target CNC
        if entity_dict['RGV'].posi == (target_cnc + 1) // 2:
            if (entity_dict['CNC'][target_cnc].status
                    == cnc.CNC_modecode_rev['processing']):
                return rgv.RGV_modecode_rev['idle']
            else:
                alg.index += 1   # cargo supplied
                if target_cnc % 2:
                    return rgv.RGV_modecode_rev['supply cargo 1']
                else:
                    return rgv.RGV_modecode_rev['supply cargo 2']
        else:
            steps = (target_cnc + 1) // 2 - entity_dict['RGV'].posi
            return rgv.RGV_modecode_rev['move ' + str(steps)]

    alg.chromosome = chromosome
    alg.index = 0   # subscript the chromosome
    return alg


if __name__ == '__main__':
    test_chromosome = np.random.randint(1, 9, 200, 'int64')
    print(test_chromosome)
    simulator = world.World(decode(test_chromosome), 3600 * 8)
    simulator.simulate()
