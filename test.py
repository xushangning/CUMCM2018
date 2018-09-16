import alg1_1
import world

simulator = world.World(alg1_1.PriorityListAlgorithm().alg, [0, 0, 0, 0, 0, 0, 0, 0], 3600 * 8, True)
simulator.simulate()

# print(alg1_1.genetic_list)
simulator.final()

res_1 = [0] * 500
res_2 = [0] * 500
res_3 = [0] * 500
res_4 = [0] * 500
res_5 = [0] * 500
res_6 = [0] * 500
with open("fail-6-1.csv", "w") as f:
    for up in simulator.up_log:
        if res_1[up['id']] == 0:
            res_1[up['id']] = up
        else:
            res_2[up['id']] = up
    for down in simulator.down_log:
        if res_3[down['id']] == 0:
            res_3[down['id']] = down
        else:
            res_4[down['id']] = down
    i = 0
    for a, b, c, d in zip(res_1, res_2, res_3, res_4):
        if a != 0 and c != 0:
            i += 1
            f.write("{},{},{}\n".format(a['cnc'], a['time'], c['time']))

    print(i)
