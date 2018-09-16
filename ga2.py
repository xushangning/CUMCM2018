import numpy as np
import multiprocessing
import random

import cnc
import rgv
import world
import cargo
from ga import select_new_population, crossover


def decode(chromosome_pair):
    def alg(entity_dict, clock):
        if entity_dict['RGV'].carry is not None:
            if (entity_dict['RGV'].carry.status
                    == cargo.Cargo_modecode_rev['ready']):
                return rgv.RGV_modecode_rev['wash']
            elif (entity_dict['RGV'].carry.status
                    == cargo.Cargo_modecode_rev['half']):
                # indicate whether the chosen CNC comes from the first
                # chromosome or the second chromosome
                chosen_cnc_index = 1
        # choose between two CNCs
        else:
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
                if steps[0]:
                    waiting_time[0] += rgv.RGV_param[
                        rgv.RGV_modecode_rev['move ' + str(steps[0])]]
                if steps[1]:
                    waiting_time[1] += rgv.RGV_param[
                        rgv.RGV_modecode_rev['move ' + str(steps[1])]]
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
                if target_cnc % 2:
                    command = rgv.RGV_modecode_rev['supply cargo 1']
                else:
                    command = rgv.RGV_modecode_rev['supply cargo 2']
        return command

    alg.chromosome = chromosome_pair
    alg.index = [0, 0]  # 2 subscripts for 2 chromosomes
    return alg


def initial_population(encode_length, population_size, sample_space):
    chromosomes = np.array([
        np.array([sample_space[i] for i in np.random.randint(
            len(sample_space), size=encode_length)], 'int8')
        for _ in range(population_size)
    ], 'int8')
    return chromosomes


class SimmapFunctor:
    def __init__(self, template):
        self.template = template

    def simmmap(self, chromosome_pair):
        simulator = world.World(
            decode(chromosome_pair), self.template, 3600 * 8)
        simulator.simulate()
        return simulator.total()


def fitness(chromosome_pairs, template):
    # 得到种群规模和决策变量的个数
    population_size = chromosome_pairs.shape[1]
    # 初始化种群的适应度值为0
    fitness_values = np.zeros(population_size)
    # 计算适应度值
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    # for i in range(population):
    #     simulator = world.World(decode(chromosomes[i]), 3600 * 8)
    #     simulator.simulate()
    #     fitness_values[i] = simulator.total()
    fitness_values = pool.map(
        SimmapFunctor(template).simmmap,
        np.transpose(chromosome_pairs, (1, 0, 2))
    )
    # 计算每个染色体被选择的概率
    probability = np.exp(fitness_values) / np.sum(np.exp(fitness_values))
    # 得到每个染色体被选中的累积概率
    cum_probability = np.cumsum(probability)
    return fitness_values, cum_probability


def mutation(population, DNA_bases, Pm=0.05):
    """
    :param population: 经交叉后得到的种群
    :param Pm: 变异概率默认是0.01
    :return: 经变异操作后的新种群
    """
    update_population = np.copy(population)
    m, n = population.shape
    # 计算需要变异的基因个数
    gene_num = np.uint8(m * n * Pm)
    # 将所有的基因按照序号进行10进制编码，则共有m*n个基因
    # 随机抽取gene_num个基因进行基本位变异
    mutationGeneIndex = random.sample(range(0, m * n), gene_num)
    # 确定每个将要变异的基因在整个染色体中的基因座(即基因的具体位置)
    for gene in mutationGeneIndex:
        # 确定变异基因位于第几个染色体
        chromosomeIndex = gene // n
        # 确定变异基因位于当前染色体的第几个基因位
        geneIndex = gene % n
        # mutation
        update_population[chromosomeIndex, geneIndex] = DNA_bases[
            np.random.randint(len(DNA_bases), dtype='int')
        ]
    return update_population


def ga2(DNA_bases_group, template, max_iter):
    chromosome_length = 200
    chromosome_pairs = np.array([
        initial_population(chromosome_length, 50, DNA_bases_group[0]),
        initial_population(chromosome_length, 50, DNA_bases_group[1])
    ], 'int8')

    for iteration in range(max_iter):
        cum_proba = fitness(chromosome_pairs, template)[1]
        new_populations = np.array([
            select_new_population(chromosome_pairs[0], cum_proba),
            select_new_population(chromosome_pairs[1], cum_proba),
        ], 'int8')
        crossover_population = np.array([
            crossover(new_populations[0]),
            crossover(new_populations[1])
        ], 'int8')
        mutated_population = np.array([
            mutation(crossover_population[0], DNA_bases_group[0]),
            mutation(crossover_population[1], DNA_bases_group[1])
        ], 'int8')
        chromosome_pairs = mutated_population
        fitness_values = fitness(chromosome_pairs, template)[0]
        fitness_values.sort()
        print(iteration, fitness_values)


if __name__ == '__main__':
    template = [1, 2, 2, 1, 1, 1, 2, 2]
    cnc_type = [[1, 4, 5, 6], [2, 3, 7, 8]]
    ga2(cnc_type, template, 10)
