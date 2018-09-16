# The idiot demo for problem 2_1, no algorithm at all

RGV_modecode_rev = {
    'idle': 0,
    'move 1 left': 1,
    'move 1 right': 2,
    'move 2 left': 3,
    'move 2 right': 4,
    'move 3 left': 5,
    'move 3 right': 6,
    'supply cargo 1': 7,
    'supply cargo 2': 8,
    'wash': 9
}

Cargo_modecode_rev = {
    'raw': 0,
    'half': 1,
    'ready': 2,
    'done': 3
}

genetic_list = [[], []]

class PriorityListAlgorithm:
    def __init__(self):
        # parameters
        self.proc_time = 3600 * 8
        self.clockCycle = 1
        self.commands = []
        # default list of priority
        self.priorList = {
            "Prepare0odd": 0, # go and load first step
            "Prepare0even": 1,
            "Prepare1odd": 2,
            "Prepare1even": 3,
            "Prepare2odd": 4,
            "Prepare2even": 5,
            "Prepare3odd": 6,
            "Prepare3even": 7,
            "Load0odd": 8,  # go and load second step (without washing)
            "Load0even": 9,
            "Load1odd": 10,
            "Load1even": 11,
            "Load2odd": 12,
            "Load2even": 13,
            "Load3odd": 14,
            "Load3even": 15,
            "Take0odd": 16,  # go and load second step (with washing)
            "Take0even": 17,
            "Take1odd": 18,
            "Take1even": 19,
            "Take2odd": 20,
            "Take2even": 21,
            "Take3odd": 22,
            "Take3even": 23,
            "WaitNext": 24,  # go to waiting position
        }

    def alg(self, entity_dict, clock):
        """
        :param entity_dict: entity_dict of world.py
        :return: method code
        """
        rgvPosition = entity_dict['RGV'].posi
        if not self.commands:
            self.commands = self.getCommand(entity_dict)
            currentCommand = self.commands[0]
            self.nextCommand()
            if currentCommand == 7:
                cncPosition = rgvPosition * 2 - 1
                if cncPosition in [1, 4, 5, 6]:
                    genetic_list[0].append(cncPosition)
                else:
                    genetic_list[1].append(cncPosition)
            if currentCommand == 8:
                cncPosition = rgvPosition * 2
                if cncPosition in [1, 4, 5, 6]:
                    genetic_list[0].append(cncPosition)
                else:
                    genetic_list[1].append(cncPosition)

            return currentCommand
        else:
            currentCommand = self.commands[0]
            self.nextCommand()
            if currentCommand == 7:
                cncPosition = rgvPosition * 2 - 1
                if cncPosition in [1, 4, 5, 6]:
                    genetic_list[0].append(cncPosition)
                else:
                    genetic_list[1].append(cncPosition)
            if currentCommand == 8:
                cncPosition = rgvPosition * 2
                if cncPosition in [1, 4, 5, 6]:
                    genetic_list[0].append(cncPosition)
                else:
                    genetic_list[1].append(cncPosition)
            return currentCommand

    # add a command to the command queue
    def getCommand(self, entity_dict):
        commandQueue = [0 for x in range(0, 24)]
        cncStatus = entity_dict['CNC']  # get the status of all CNCs
        rgvStatus = entity_dict['RGV']  # same as above
        rgvPosition = rgvStatus.posi  # the position of RGV

        for cncNum in range(1, len(cncStatus)):
            cnc = cncStatus[cncNum]
            # if the cnc is going to process the non-processed cargo
            if cnc.proc_mode == 1:
                if rgvStatus.carry:
                    if rgvStatus.carry.status == Cargo_modecode_rev['half']:
                        continue
                if cnc.status == 1:
                    continue
                cncPosition = (cncNum + 1) // 2

                if cncNum % 2 == 0:  # judge the odevity of CNC
                    OEproperty = "even"
                else:
                    OEproperty = "odd"

                if cncPosition - rgvPosition < 0:  # judge the direction RGV is going
                    direction = "left"
                elif cncPosition - rgvPosition > 0:
                    direction = "right"
                else:
                    direction = False

                commandCode = []  # save the bunch of command code

                command = "Prepare" + str(abs(rgvPosition - cncPosition)) + OEproperty
                commandPriority = self.priorList[command]

                if not direction:
                    if OEproperty == "even":
                        commandCode.append(8)  # append the even one
                    else:
                        commandCode.append(7)  # append the odd one
                else:
                    moveCommand = "move " + str(abs(rgvPosition - cncPosition)) + " " + direction
                    commandCode.append(RGV_modecode_rev[moveCommand])  # append the code for moveCommand
                    if OEproperty == "even":
                        commandCode.append(8)  # append the even one
                    else:
                        commandCode.append(7)  # append the odd one

            # if the cnc is going to process the half-completed cargo
            if cnc.proc_mode == 2: 
                if cnc.status == 1:
                    continue
                if not rgvStatus.carry:
                    continue
                if rgvStatus.carry.status != Cargo_modecode_rev['half']:
                    continue
                cncPosition = (cncNum + 1) // 2  # the position of the current CNC

                if cncNum % 2 == 0:  # judge the odevity of CNC
                    OEproperty = "even"
                else:
                    OEproperty = "odd"

                if cncPosition - rgvPosition < 0:   # judge the direction RGV is going
                    direction = "left"
                elif cncPosition - rgvPosition > 0:
                    direction = "right"
                else:
                    direction = False

                commandCode = []    # save the bunch of command code

                # judge the status of CNC
                if cnc.status == 0:
                    # if the cnc is empty(idle), pure load
                    command = "Load" + str(abs(rgvPosition - cncPosition)) + OEproperty
                    commandPriority = self.priorList[command]

                    if not direction:
                        if OEproperty == "even":
                            commandCode.append(8)    # append the even one
                        else:
                            commandCode.append(7)    # append the odd one
                    else:
                        moveCommand = "move " + str(abs(rgvPosition - cncPosition)) + " " + direction
                        commandCode.append(RGV_modecode_rev[moveCommand])    # append the code for moveCommand
                        if OEproperty == "even":
                            commandCode.append(8)    # append the even one
                        else:
                            commandCode.append(7)    # append the odd one

                else:
                    # if the cnc is done working, load then wash
                    command = "Take" + str(abs(rgvPosition - cncPosition)) + OEproperty
                    commandPriority = self.priorList[command]
                    if not direction:
                        if OEproperty == "even":
                            commandCode.append(8)    # append the even one
                        else:
                            commandCode.append(7)    # append the odd one
                    else:
                        moveCommand = "move " + str(abs(rgvPosition - cncPosition)) + " " + direction
                        commandCode.append(RGV_modecode_rev[moveCommand])    # append the code for moveCommand
                        if OEproperty == "even":
                            commandCode.append(8)    # append the even one
                        else:
                            commandCode.append(7)    # append the odd one
                    # wash process
                    commandCode.append(9)    # append the wash process (depending on rgv.py)

            # load the commandCode into commandQueue
            commandQueue[commandPriority] = commandCode

        for commands in commandQueue:
            if commands != 0:
                return commands

        return [0]

    # get the first command in the command list, and then erase it
    def nextCommand(self):
        self.commands = self.commands[1:]
        return

