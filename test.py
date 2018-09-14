import alg1_1
import world

simulator = world.World(alg1_1.PriorityListAlgorithm().alg, 3600*8)
simulator.simulate()
