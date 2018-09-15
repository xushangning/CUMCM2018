from cargo import Cargo_modecode, Cargo_modecode_rev
import random

CNC_proctime_1 = 560
CNC_proctime_2 = 378

CNC_modecode = {
    0: 'idle',
    1: 'processing',
    2: 'processed',
    3: 'down'
}

CNC_modecode_rev = {
    'idle': 0,
    'processing': 1,
    'processed': 2,
    'down': 3
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
    def __init__(self, proc_time, proc_type, enable_failure):
        self.proc_time = proc_time
        self.proc_mode = proc_type

        self.clock = 0
        self.status = 0
        self.proc = None  # cargo
        self.proc_clock = -1

        self.enable_failure = enable_failure
        self.will_fail = False
        self.fail_time = -1
        self.recover_time = -1

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

                if self.enable_failure:
                    dice = random.randint(1, 100)
                    if dice == 1:
                        # Will fail!
                        self.will_fail = True
                        self.fail_time = random.randint(1, self.proc_time)
                        self.recover_time = random.randint(1200, 2400)
        self.status = modecode
        return 0, None

    def update(self):
        self.clock += 1

        if self.status == CNC_modecode_rev['processing']:
            self.proc_clock -= 1

            if self.enable_failure and self.will_fail and self.proc_clock == self.fail_time:
                # It fails!
                self.status = CNC_modecode_rev['down']
                self.proc_clock = self.recover_time
                tmp_c = self.proc
                self.proc = None
                return self.status, tmp_c
        elif self.status == CNC_modecode_rev['down']:
            self.proc_clock -= 1

        if self.proc_clock == 0:
            self.proc_clock = -1

            if self.status == CNC_modecode_rev['processing']:
                tmp = self.status
                self.status = CNC_modecode_rev['processed']

                if self.proc_mode == CNC_typecode_rev['from raw to ready']:
                    self.proc.status = Cargo_modecode_rev['ready']
                elif self.proc_mode == CNC_typecode_rev['from raw to half']:
                    self.proc.status = Cargo_modecode_rev['half']
                elif self.proc_mode == CNC_typecode_rev['from half to ready']:
                    self.proc.status = Cargo_modecode_rev['ready']
                return tmp, self.proc

            elif self.status == CNC_modecode_rev['down']:
                self.status = CNC_modecode_rev['idle']
                self.will_fail = False
                self.fail_time = -1
                self.recover_time = -1
                return self.status, None

        return None, None
