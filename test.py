import alg2_1
import world

simulator = world.World(alg2_1.PriorityListAlgorithm().alg, [1, 2, 1, 2, 1, 2, 1, 2],3600*8)
simulator.simulate()
