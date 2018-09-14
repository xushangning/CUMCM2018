CNC_proctime_1 = 560
CNC_proctime_2 = 378

CNC_modecode = {
    0: 'idle',
    1: 'processing',
}

CNC_modecode_rev = {
    'idle': 0,
    'processing': 1
}


class CNC:
    def __init__(self, proc_time):
        self.proc_time = proc_time

        self.clock = 0
        self.status = 0
        self.proc_id = 0  # cargo
        self.proc_clock = -1

    def inst(self):
        pass

    def update(self):
        self.clock += 1

        if self.status == CNC_modecode_rev['processing']:
            self.proc_clock -= 1
            if self.proc_clock == 0:
                pass
