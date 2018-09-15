import alg2_1
import world

simulator = world.World(alg2_1.PriorityListAlgorithm().alg, 3600*8)
simulator.simulate()
