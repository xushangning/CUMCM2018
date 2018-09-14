RGV_param = [
    -1,
    20,
    20,
    33,
    33,
    46,
    46,
    28,
    31,
    25
]

RGV_modecode = {
    0: 'idle',
    1: 'move 1 left',
    2: 'move 1 right',
    3: 'move 2 left',
    4: 'move 2 right',
    5: 'move 3 left',
    6: 'move 3 right',
    7: 'supply cargo 1',
    8: 'consume cargo 1',
    9: 'supply cargo 2',
    10: 'consume cargo 2',
    11: 'wash'
}

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


class RGV:
    def __init__(self, vec_t, cnc_api):
        self.time = vec_t  # should be a vector of length 12

        self.clock = 0
        self.status = RGV_modecode_rev['idle']
        self.proc_clock = -1

        self.posi = 1  # 1,2,3,4
        self.carry_id = 0

        self.cnc = cnc_api

    def inst(self, modecode, cid):
        # check the validity of instruction
        if RGV_modecode[modecode] == 'move 1 left':
            if self.posi <= 1:
                return -1
        elif RGV_modecode[modecode] == 'move 1 right':
            if self.posi >= 4:
                return -1
        elif RGV_modecode[modecode] == 'move 2 left':
            if self.posi <= 2:
                return -1
        elif RGV_modecode[modecode] == 'move 2 right':
            if self.posi >= 3:
                return -1
        elif RGV_modecode[modecode] == 'move 3 left':
            if self.posi <= 3:
                return -1
        elif RGV_modecode[modecode] == 'move 3 right':
            if self.posi >= 2:
                return -1
        elif RGV_modecode[modecode] == 'supply cargo 1':
            if self.cnc['status'](self.posi, 1) != 0:
                return -1
            self.carry_id = cid
        elif RGV_modecode[modecode] == 'consume cargo 1':
            if self.cnc['status'](self.posi, 1) != 2:
                return -1
        elif RGV_modecode[modecode] == 'supply cargo 2':
            if self.cnc['status'](self.posi, 2) != 0:
                return -1
            self.carry_id = cid
        elif RGV_modecode[modecode] == 'consume cargo 2':
            if self.cnc['status'](self.posi, 2) != 2:
                return -1

        self.status = modecode
        self.proc_clock = RGV_param[modecode]

    def update(self):
        self.clock += 1

        if self.status == RGV_modecode_rev['idle']:
            return self.status, None
        else:
            self.proc_clock -= 1

        if self.proc_clock == 0:
            tmp = self.status
            self.status = RGV_modecode_rev['idle']
            self.proc_clock = -1
            if tmp == RGV_modecode_rev['move 1 left']:
                self.posi -= 1
                return tmp, None
            elif tmp == RGV_modecode_rev['move 1 right']:
                self.posi += 1
                return tmp, None
            elif tmp == RGV_modecode_rev['move 2 left']:
                self.posi -= 2
                return tmp, None
            elif tmp == RGV_modecode_rev['move 2 right']:
                self.posi += 2
                return tmp, None
            elif tmp == RGV_modecode_rev['move 3 left']:
                self.posi -= 3
                return tmp, None
            elif tmp == RGV_modecode_rev['move 3 right']:
                self.posi += 3
                return tmp, None
            elif tmp == RGV_modecode_rev['supply cargo 1']:
                tmp_id = self.carry_id
                self.carry_id = 0
                self.cnc['supply'](self.posi, 1, tmp_id)
                return tmp, tmp_id
            elif tmp == RGV_modecode_rev['supply cargo 2']:
                tmp_id = self.carry_id
                self.carry_id = 0
                self.cnc['supply'](self.posi, 2, tmp_id)
                return tmp, tmp_id
            elif tmp == RGV_modecode_rev['consume cargo 1']:
                self.carry_id = self.cnc['consume'](self.posi, 1)
                return tmp, self.carry_id
            elif tmp == RGV_modecode_rev['consume cargo 2']:
                self.carry_id = self.cnc['consume'](self.posi, 2)
                return tmp, self.carry_id
            elif tmp == RGV_modecode_rev['wash']:
                return tmp, self.carry_id

        return None, None
