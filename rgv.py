from cargo import Cargo_modecode, Cargo_modecode_rev
import cnc

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
    25,
]

RGV_modecode = {
    0: 'idle',
    1: 'move -1',
    2: 'move 1',
    3: 'move -2',
    4: 'move 2',
    5: 'move -3',
    6: 'move 3',
    7: 'supply cargo 1',
    8: 'supply cargo 2',
    9: 'wash'
}

RGV_modecode_rev = {
    'idle': 0,
    'move -1': 1,
    'move 1': 2,
    'move -2': 3,
    'move 2': 4,
    'move -3': 5,
    'move 3': 6,
    'supply cargo 1': 7,
    'supply cargo 2': 8,
    'wash': 9
}


class RGV:
    def __init__(self, vec_t, cnc_api):
        self.time = vec_t  # should be a vector of length 12

        self.clock = 0
        self.status = RGV_modecode_rev['idle']
        self.proc_clock = -1

        self.posi = 1  # 1,2,3,4
        self.carry = None
        self.last_inst = 0
        self.inst_list = []

        self.cnc = cnc_api

    def inst(self, modecode, cargo_t):
        last_t = None

        # check the validity of instruction
        if RGV_modecode[modecode] == 'move -1':
            if self.posi <= 1:
                return -1, None
        elif RGV_modecode[modecode] == 'move 1':
            if self.posi >= 4:
                return -1, None
        elif RGV_modecode[modecode] == 'move -2':
            if self.posi <= 2:
                return -1, None
        elif RGV_modecode[modecode] == 'move 2':
            if self.posi >= 3:
                return -1, None
        elif RGV_modecode[modecode] == 'move -3':
            if self.posi <= 3:
                return -1, None
        elif RGV_modecode[modecode] == 'move 3':
            if self.posi >= 2:
                return -1, None
        elif RGV_modecode[modecode] == 'supply cargo 1':
            if self.cnc['status'](self.posi, 1) == cnc.CNC_modecode_rev['processing']:
                return -1, None
            elif self.cnc['status'](self.posi, 1) == cnc.CNC_modecode_rev['down']:
                return -1, None

            if cargo_t is not None:
                self.carry = cargo_t
            elif self.carry is None:
                return -1, None

            last_t = self.cnc['curr'](self.posi, 1)
        elif RGV_modecode[modecode] == 'supply cargo 2':
            if self.cnc['status'](self.posi, 2) == cnc.CNC_modecode_rev['processing']:
                return -1, None
            elif self.cnc['status'](self.posi, 2) == cnc.CNC_modecode_rev['down']:
                return -1, None

            if cargo_t is not None:
                self.carry = cargo_t
            elif self.carry is None:
                return -1, None
            last_t = self.cnc['curr'](self.posi, 2)
        elif RGV_modecode[modecode] == 'wash':
            if self.carry is None or \
                    self.carry.status != Cargo_modecode_rev['ready']:
                return -1, None

        self.status = modecode
        if self.status != 0:
            self.inst_list.append(self.status)
        self.proc_clock = RGV_param[modecode]
        return 0, last_t

    def update(self):
        self.clock += 1

        if self.status == RGV_modecode_rev['idle']:
            return self.status, None
        else:
            self.proc_clock -= 1

        if self.proc_clock == 0:
            self.last_inst = self.status
            tmp = self.status
            self.status = RGV_modecode_rev['idle']
            self.proc_clock = -1
            if tmp == RGV_modecode_rev['move -1']:
                self.posi -= 1
                return tmp, None
            elif tmp == RGV_modecode_rev['move 1']:
                self.posi += 1
                return tmp, None
            elif tmp == RGV_modecode_rev['move -2']:
                self.posi -= 2
                return tmp, None
            elif tmp == RGV_modecode_rev['move 2']:
                self.posi += 2
                return tmp, None
            elif tmp == RGV_modecode_rev['move -3']:
                self.posi -= 3
                return tmp, None
            elif tmp == RGV_modecode_rev['move 3']:
                self.posi += 3
                return tmp, None
            elif tmp == RGV_modecode_rev['supply cargo 1']:
                tmp_t = self.carry
                self.carry = self.cnc['consume'](self.posi, 1)
                flag = self.cnc['supply'](self.posi, 1, tmp_t)
                if flag == -1:
                    return -1, None
                return tmp, tmp_t
            elif tmp == RGV_modecode_rev['supply cargo 2']:
                tmp_t = self.carry
                self.carry = self.cnc['consume'](self.posi, 2)
                flag = self.cnc['supply'](self.posi, 2, tmp_t)
                if flag == -1:
                    return -1, None
                return tmp, tmp_t
            elif tmp == RGV_modecode_rev['wash']:
                self.carry.status = Cargo_modecode_rev['done']
                tmp_t = self.carry
                self.carry = None
                return tmp, tmp_t

        return None, None
