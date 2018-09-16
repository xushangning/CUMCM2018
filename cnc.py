from cargo import Cargo_modecode, Cargo_modecode_rev

CNC_proctime_1 = 560
CNC_proctime_2 = 378

CNC_modecode = {
    0: 'idle',
    1: 'processing',
    2: 'processed'
}

CNC_modecode_rev = {
    'idle': 0,
    'processing': 1,
    'processed': 2
}

CNC_typecode = {
    0: 'from raw to ready',
    1: 'from raw to half',
    2: 'from half to ready'
}

CNC_typecode_rev = {
    'from raw to ready': 0,
    'from raw to half': 1,
    'from half to ready': 2
}


class CNC:
    def __init__(self, proc_time, proc_type):
        self.proc_time = proc_time
        self.proc_mode = proc_type

        self.clock = 0
        self.status = 0
        self.proc = None  # cargo
        self.proc_clock = -1

    def inst(self, modecode):
        if modecode == CNC_modecode_rev['processing']:
            if self.proc_mode == CNC_typecode_rev['from raw to ready'] and \
                    self.proc.status != Cargo_modecode_rev['raw']:
                return -1, None
            elif self.proc_mode == CNC_typecode_rev['from raw to half'] and \
                    self.proc.status != Cargo_modecode_rev['raw']:
                return -1, None
            elif self.proc_mode == CNC_typecode_rev['from half to ready'] and \
                    self.proc.status != Cargo_modecode_rev['half']:
                return -1, None
            else:
                self.proc_clock = self.proc_time

        self.status = modecode
        return 0, None

    def update(self):
        self.clock += 1

        if self.status == CNC_modecode_rev['processing']:
            self.proc_clock -= 1
            if self.proc_clock == 0:
                tmp = self.status
                self.status = CNC_modecode_rev['processed']
                self.proc_clock = -1

                if self.proc_mode == CNC_typecode_rev['from raw to ready']:
                    self.proc.status = Cargo_modecode_rev['ready']
                elif self.proc_mode == CNC_typecode_rev['from raw to half']:
                    self.proc.status = Cargo_modecode_rev['half']
                elif self.proc_mode == CNC_typecode_rev['from half to ready']:
                    self.proc.status = Cargo_modecode_rev['ready']
                return tmp, self.proc

        return None, None
