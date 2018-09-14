class PriorityListAlgorithm:
    def __init__(self):
        # parameters
        self.proc_time = 3600 * 8
        self.clockCycle = 1
        self.commandQueue = [0 for x in range(0, 17)]

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

    def alg(self, entity_dict):
        """
        :param entity_dict: entity_dict of world.py
        :return: method code
        """

    # add a command to the command queue
    def addCommand(self, entity_dict):
        cncStatus = entity_dict['CNC']  # get the status of all CNCs
        rgvStatus = entity_dict['RGV']  # same as above
        rgvPosition = rgvStatus.posi  # the position of RGV

        for cncNum in range(1, 1 + len(cncStatus)):
            cnc = cncStatus[cncNum - 1]
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

            commandcode = []    # save the bunch of command code

            if cnc.status == 0:
                # if the cnc is empty(idle), pure load
                command = "Load" + str(abs(rgvPosition - cncPosition)) + OEproperty
                if not direction:
                    return  # 18:00

            else:
                # if the cnc is done working, take then load
                command = "Take" + str(abs(rgvPosition - cncPosition)) + OEproperty
            commandPriority = self.priorList[command]

        return

    # erase the command that is executed
    def eraseCommand(self):
        self.commandQueue = self.commandQueue[1:]
        return
