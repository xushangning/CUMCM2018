import numpy as np
import rgv
import cnc

# parameters
proc_time = 3600*8
clockCycle = 1
commandQueue = list()
completeWork = 0
controller = cnc.CNC(proc_time)
vehicle = rgv.RGV([x for x in range(1, 13)], controller)

# default list of priority
priorList = {
    "Load0odd": 1,
    "Load0even": 1.5,
    "Load1odd": 2,    # go and load in one step
    "Load1even": 2.5,
    "Load2odd": 3,
    "Load2even": 3.5,
    "Load3odd": 4,
    "Load3even":4.5,
    "Take0odd": 5,    # take and load in one step
    "Take0even": 5.5,
    "Take1odd": 6,
    "Take1even": 6.5,
    "Take2odd": 7,
    "Take2even":7.5,
    "Take3odd": 8,
    "Take3even": 8.5,
    "WaitNext": 9,  # go to waiting position
}


# the status of CNCs
def cncStatus():
    return


# add a command to the command queue
def addCommand(command):
    commandQueue.append(command)
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
