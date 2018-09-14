import numpy as np
import world

# parameters
proc_time = 3600*8
clockCycle = 1
commandQueue = list()
completeWork = 0
simulator = world.World(proc_time)

# default list of priority
priorList = {
    "Load0odd": 1,
    "Load0even": 1.5,
    "Load1odd": 2,    # go and load in one step
    "Load1even": 2.5,
    "Load2odd": 3,
    "Load2even": 3.5,
    "Load3odd": 4,
    "Load3even": 4.5,
    "Take0odd": 5,    # take and load in one step
    "Take0even": 5.5,
    "Take1odd": 6,
    "Take1even": 6.5,
    "Take2odd": 7,
    "Take2even": 7.5,
    "Take3odd": 8,
    "Take3even": 8.5,
    "WaitNext": 9,  # go to waiting position
}


# add a command to the command queue
def addCommand():
    cncStatus = simulator.entity_dict['CNC']    # get the status of all CNCs
    rgvStatus = simulator.entity_dict['RGV']    # same as above
    rgvPosition = rgvStatus.posi                # the position of RGV
    for cncNum in range(1, 1 + len(cncStatus)):
        cnc = cncStatus[cncNum - 1]
        if cnc.status == 1:
            continue
        cncPosition = (cncNum + 1) // 2         # the position of the current CNC
        if cncNum % 2 == 0:                     # judge the odevity of CNC
            OEproperty = "even"
        else:
            OEproperty = "odd"
        
    return


# the position RGV goes to when waiting
def nextWorkPosition():
    return


# the next move of RGV
def nextMove():
    vehicle.update()
    if vehicle.status == rgv.RGV_modecode_rev['idle']:
        nextMove = commandQueue[0]
        commandQueue = commandQueue[1:]


def main():
    clock = 0
    while clock < proc_time:
        addCommand()
        nextMove()
        clock += clockCycle
    print(completeWork)
