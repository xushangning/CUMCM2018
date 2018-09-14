# note
# CNC have no control over its cargo

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


class CNC:
    def __init__(self, proc_time):
        self.proc_time = proc_time

        self.clock = 0
        self.status = 0
        self.proc_id = 0  # cargo
        self.proc_clock = -1

    def inst(self, modecode):
        self.status = modecode
        if modecode == CNC_modecode_rev['processing']:
            self.proc_clock = self.proc_time

    def update(self):
        self.clock += 1

        if self.status == CNC_modecode_rev['processing']:
            self.proc_clock -= 1
            if self.proc_clock == 0:
                tmp = self.status
                self.status = CNC_modecode_rev['processed']
                self.proc_clock = -1
                return tmp, self.proc_id

        return None, None
