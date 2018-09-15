import numpy as np
import random

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

        # if the last instruction is supplying cargo, then do the washing,
        # except that the cargo is the first one supplied to the CNC
        if ((entity_dict['RGV'].last_inst
                == rgv.RGV_modecode_rev['supply cargo 1']
                or entity_dict['RGV'].last_inst
                == rgv.RGV_modecode_rev['supply cargo 2'])
                and alg.should_wash):
            return rgv.RGV_modecode_rev['wash']
        # if RGV is right in front of the target CNC
        elif entity_dict['RGV'].posi == (target_cnc + 1) // 2:
            if (entity_dict['CNC'][target_cnc].status
                    == cnc.CNC_modecode_rev['processing']):
                return rgv.RGV_modecode_rev['idle']
            else:
                alg.index += 1   # cargo supplied
                # if this is the first cargo supplied to the CNC
                # DON'T WASH
                if (entity_dict['CNC'][target_cnc].status
                        == cnc.CNC_modecode_rev['idle']):
                    alg.should_wash = False
                else:
                    alg.should_wash = True
                if target_cnc % 2:
                    return rgv.RGV_modecode_rev['supply cargo 1']
                else:
                    return rgv.RGV_modecode_rev['supply cargo 2']
        else:
            steps = (target_cnc + 1) // 2 - entity_dict['RGV'].posi
            return rgv.RGV_modecode_rev['move ' + str(steps)]

    alg.chromosome = chromosome
    alg.index = 0   # subscript the chromosome
    # whether supplying cargo should be followed by washing
    alg.should_wash = False
    return alg


def initial_population(encode_length, population_size):
    chromosomes = np.random.randint(
        1, 9, (population_size, encode_length), 'int8')
    return chromosomes


def fitness(chromosomes):
    # 得到种群规模和决策变量的个数
    population = chromosomes.shape[0]
    # 初始化种群的适应度值为0
    fitness_values = np.zeros(population)
    # 计算适应度值
    for i in range(population):
        simulator = world.World(decode(chromosomes[i]), 3600 * 4)
        simulator.simulate()
        fitness_values[i] = simulator.total()
    # 计算每个染色体被选择的概率
    probability = np.exp(fitness_values) / np.sum(np.exp(fitness_values))
    # 得到每个染色体被选中的累积概率
    cum_probability = np.cumsum(probability)
    return fitness_values, cum_probability


def select_new_population(chromosomes, cum_probability):
    new_population = np.zeros(chromosomes.shape, 'int8')
    m, n = chromosomes.shape
    # 随机产生M个概率值
    randoms = np.random.rand(m)
    for i, randoma in enumerate(randoms):
        logical = cum_probability >= randoma
        index = np.where(logical == 1)
        # index是tuple,tuple中元素是ndarray
        new_population[i, :] = chromosomes[index[0][0], :]
    return new_population


def crossover(population, pc=0.8):
    """
    :param population: 新种群
    :param pc: 交叉概率默认是0.8
    :return: 交叉后得到的新种群
    """
    # 根据交叉概率计算需要进行交叉的个体个数
    m, n = population.shape
    numbers = np.uint8(m * pc)
    # 确保进行交叉的染色体个数是偶数个
    if numbers % 2:
        numbers += 1
    # 交叉后得到的新种群
    update_population = np.zeros(population.shape, dtype=np.uint8)
    # 产生随机索引
    index = random.sample(range(m), numbers)
    # 不进行交叉的染色体进行复制
    for i in range(m):
        if not index.__contains__(i):
            update_population[i, :] = population[i, :]
    # crossover
    while len(index) > 0:
        a = index.pop()
        b = index.pop()
        # 随机产生一个交叉点
        crossover_point = random.sample(range(1, n), 1)
        crossover_point = crossover_point[0]
        # one-single-point crossover
        update_population[a, 0:crossover_point] = population[a, 0:crossover_point]
        update_population[a, crossover_point:] = population[b, crossover_point:]
        update_population[b, 0:crossover_point] = population[b, 0:crossover_point]
        update_population[b, crossover_point:] = population[a, crossover_point:]
    return update_population


def mutation(population, Pm=0.01):
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
        update_population[chromosomeIndex, geneIndex] = np.random.randint(
            1, 9, update_population.dtype)
    return update_population


def ga(max_iter):
    chromosome_length = 200
    chromosomes = initial_population(chromosome_length, 30)
    for iteration in range(max_iter):
        cum_proba = fitness(chromosomes)[1]
        new_populations = select_new_population(chromosomes, cum_proba)
        crossover_population = crossover(new_populations)
        mutated_population = mutation(crossover_population)
        chromosomes = mutated_population

    print(fitness(chromosomes)[0])


if __name__ == '__main__':
    ga(10)
