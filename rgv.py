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
    def __init__(self, vec_t, alg):
        self.time = vec_t

        self.clock = 0
        self.status = RGV_modecode_rev['idle']
        self.proc_clock = -1

        self.posi = 1  # 1,2,3,4
        self.carry_id = 0

        self.alg = alg  # algorithm, a function pointer

    def update(self):
        self.clock += 1

        if self.status != RGV_modecode_rev['idle']:
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
            elif tmp == RGV_modecode_rev['supply cargo 1'] or tmp == RGV_modecode_rev['supply cargo 2']:
                tmp_id = self.carry_id
                self.carry_id = 0
                return tmp, tmp_id

        return None, None
