# The idiot demo for problem 1_1, no algorithm at all
# First draft on Sept.14, 20:12
# Command code to be added in Line 82-112, depending on rgv.py
# Sept.14, 22:10, notice that the entity_dict["CNC"] starts with a -1.

RGV_modecode_rev = {
    'idle': 0,
    'move 1 left': 1,
    'move 1 right': 2,
    'move 2 left': 3,
    'move 2 right': 4,
    'move 3 left': 5,
    'move 3 right': 6,
    'supply cargo 1': 7,
    'consume cargo 1': 8,
    'supply cargo 2': 9,
    'consume cargo 2': 10,
    'wash': 11
}


class PriorityListAlgorithm:
    def __init__(self):
        # parameters
        self.proc_time = 3600 * 8
        self.clockCycle = 1
        self.commands = []
        # default list of priority
        self.priorList = {
            "Load0odd": 0,
            "Load0even": 1,
            "Load1odd": 2,  # go and load in one step
            "Load1even": 3,
            "Load2odd": 4,
            "Load2even": 5,
            "Load3odd": 6,
            "Load3even": 7,
            "Take0odd": 8,  # take and load in one step
            "Take0even": 9,
            "Take1odd": 10,
            "Take1even": 11,
            "Take2odd": 12,
            "Take2even": 13,
            "Take3odd": 14,
            "Take3even": 15,
            "WaitNext": 16,  # go to waiting position
        }

    def alg(self, entity_dict, clock):
        """
        :param entity_dict: entity_dict of world.py
        :return: method code
        """
        if not self.commands:
            self.commands = self.getCommand(entity_dict)
            currentCommand = self.commands[0]
            self.nextCommand()
            return currentCommand
        else:
            currentCommand = self.commands[0]
            self.nextCommand()
            return currentCommand

    # add a command to the command queue
    def getCommand(self, entity_dict):
        commandQueue = [0 for x in range(0, 17)]
        cncStatus = entity_dict['CNC']  # get the status of all CNCs
        rgvStatus = entity_dict['RGV']  # same as above
        rgvPosition = rgvStatus.posi  # the position of RGV

        for cncNum in range(1, 1 + len(cncStatus)):
            cnc = cncStatus[cncNum]
            if cnc.status == 1:
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
                direction = None

            commandCode = []    # save the bunch of command code

            # judge the status of CNC
            if cnc.status == 0:
                # if the cnc is empty(idle), pure load
                command = "Load" + str(abs(rgvPosition - cncPosition)) + OEproperty
                commandPriority = self.priorList[command]

                if not direction:
                    if OEproperty == "even":
                        commandCode.append(7)    # append the even one
                    else:
                        commandCode.append(8)    # append the odd one
                else:
                    moveCommand = "move " + str(int(abs(cncPosition))) + " " + direction
                    commandCode.append(RGV_modecode_rev[moveCommand])    # append the code for moveCommand
                    if OEproperty == "even":
                        commandCode.append(7)    # append the even one
                    else:
                        commandCode.append(8)    # append the odd one

            else:
                # if the cnc is done working, load then wash
                command = "Take" + str(abs(rgvPosition - cncPosition)) + OEproperty
                commandPriority = self.priorList[command]
                if not direction:
                    if OEproperty == "even":
                        commandCode.append(7)    # append the even one
                    else:
                        commandCode.append(8)    # append the odd one
                else:
                    moveCommand = "move " + str(int(abs(cncPosition))) + " " + direction
                    commandCode.append(RGV_modecode_rev[moveCommand])    # append the code for moveCommand
                    if OEproperty == "even":
                        commandCode.append(7)    # append the even one
                    else:
                        commandCode.append(8)    # append the odd one
                # wash process
                commandCode.append(11)    # append the wash process (depending on rgv.py)

            # load the commandCode into commandQueue
            commandQueue[commandPriority] = commandCode
            for commands in commandQueue:
                if commands != 0:
                    return commands

    # get the first command in the command list, and then erase it
    def nextCommand(self):
        self.commands = self.commands[1:]
        return

