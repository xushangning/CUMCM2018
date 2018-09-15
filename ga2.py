import numpy as np

import cnc
import rgv
import world
import cargo


def decode(first_chromosome, second_chromosome):
    def alg(entity_dict, clock):
        if alg.should_wash:
            alg.should_wash = False
            return rgv.RGV_modecode_rev['wash']
        if entity_dict['RGV'].carry.status == cargo.Cargo_modecode_rev['half']:
            # indicate whether the chosen CNC comes from the first chromosome
            # or the second chromosome
            chosen_cnc_index = 1
        else:
            # choose between two CNCs
            cncs = [alg.chromosome[0][alg.index[0]],
                    alg.chromosome[1][alg.index[1]]]
            if (entity_dict['CNC'][cncs[1]].status
                    == cnc.CNC_modecode_rev['idle']):
                chosen_cnc_index = 0
            else:
                waiting_time = [0, 0]   # waiting time for 2 CNCs
                steps = [               # steps needed to move to a CNC
                    (cncs[0] + 1) // 2 - entity_dict['RGV'].posi,
                    (cncs[1] + 1) // 2 - entity_dict['RGV'].posi,
                ]
                if not steps[0]:
                    waiting_time[0] += rgv.RGV_param[
                        rgv.RGV_modecode_rev['move' + str(steps[0])]]
                if not steps[1]:
                    waiting_time[1] += rgv.RGV_param[
                        rgv.RGV_modecode_rev['move' + str(steps[1])]]
                # if a CNC is processing cargoes, consider its processing time
                if (entity_dict['CNC'][cncs[0]].status
                        == cnc.CNC_modecode_rev['processing']):
                    waiting_time[0] = max(
                        waiting_time[0], entity_dict['CNC'][cncs[0]].proc_clock)
                if (entity_dict['CNC'][cncs[1]].status
                        == cnc.CNC_modecode_rev['processing']):
                    waiting_time[1] = max(
                        waiting_time[1], entity_dict['CNC'][cncs[1]].proc_clock)
                chosen_cnc_index = int(waiting_time[0] >= waiting_time[1])

        target_cnc = alg.chromosome[
            chosen_cnc_index][alg.index[chosen_cnc_index]]
        steps = (target_cnc + 1) // 2 - entity_dict['RGV'].posi
        if steps:
            command = rgv.RGV_modecode_rev['move ' + str(steps)]
        # RGV is right in front of the target CNC
        else:
            if (entity_dict['CNC'][target_cnc].status
                    == cnc.CNC_modecode_rev['processing']):
                command = rgv.RGV_modecode_rev['idle']
            else:
                alg.index[chosen_cnc_index] += 1  # cargo supplied
                # if this is the first cargo supplied to the CNC
                # DON'T WASH
                if (entity_dict['CNC'][target_cnc].status
                        != cnc.CNC_modecode_rev['idle']):
                    alg.should_wash = True
                if target_cnc % 2:
                    command = rgv.RGV_modecode_rev['supply cargo 1']
                else:
                    command = rgv.RGV_modecode_rev['supply cargo 2']
        return command

    alg.chromosome = [first_chromosome, second_chromosome]
    alg.index = [0, 0]  # 2 subscripts for 2 chromosomes
    # whether supplying cargo should be followed by washing
    alg.should_wash = False
    return alg
