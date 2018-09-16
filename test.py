import alg2_1
import world

simulator = world.World(alg2_1.PriorityListAlgorithm().alg, [1, 2, 2, 1, 1, 1, 2, 2], 3600*8)
simulator.simulate()

print(alg2_1.genetic_list)
