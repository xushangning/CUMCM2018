import rgv
import cnc
from cargo import Cargo, Cargo_modecode


class World:
    def __init__(self, alg, total_time):
        # tricky
        self.cnc_api = {
            'status': self.cnc_check,
            'supply': self.cnc_supply,
            'consume': self.cnc_consume,
            'curr': self.cnc_current
        }

        self.alg = alg

        # init all objects
        self.entity_dict = dict()
        self.entity_dict['RGV'] = rgv.RGV(rgv.RGV_param, self.cnc_api)
        self.entity_dict['CNC'] = [
            -1,
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready']),
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready']),
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready']),
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready']),
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready']),
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready']),
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready']),
            cnc.CNC(cnc.CNC_proctime_1, cnc.CNC_typecode_rev['from raw to ready'])
        ]
        self.product = []

        # clock
        self.clock = 0
        self.total_time = total_time

        # logging
        self.cargo_id = 0
        self.up_log = []  # {'id': 1, 'time': 0}
        self.down_log = []

    def update(self):
        for name, entity in self.entity_dict.items():
            if name == 'RGV':
                event, cargo_t = entity.update()
                if event is not None:
                    # main processions
                    if event == -1:
                        return -1

                    if event != 0:
                        print(rgv.RGV_modecode[event])
                        self.info()

                    if event == rgv.RGV_modecode_rev['supply cargo 1']:
                        self.up_log.append({
                            'id': cargo_t.id,
                            'time': self.clock,
                            'cnc': self.get_cnc_id(self.entity_dict['RGV'].posi, 1)
                        })
                    elif event == rgv.RGV_modecode_rev['supply cargo 2']:
                        self.up_log.append({
                            'id': cargo_t.id,
                            'time': self.clock,
                            'cnc': self.get_cnc_id(self.entity_dict['RGV'].posi, 2)
                        })
                    elif event == rgv.RGV_modecode_rev['wash']:
                        self.product.append(cargo_t)

                    new_inst = self.alg(self.entity_dict, self.clock)
                    if new_inst == rgv.RGV_modecode_rev['supply cargo 1'] or \
                            new_inst == rgv.RGV_modecode_rev['supply cargo 2']:
                        if self.entity_dict['RGV'].carry is None:
                            self.cargo_id += 1
                            flag, opt_cargo = self.entity_dict['RGV'].inst(
                                new_inst, Cargo(self.cargo_id))
                        else:
                            flag, opt_cargo = self.entity_dict['RGV'].inst(
                                new_inst, None)
                    else:
                        flag, opt_cargo = self.entity_dict['RGV'].inst(
                            new_inst, None)
                    if flag == -1:
                        return -1

                    if new_inst == rgv.RGV_modecode_rev['supply cargo 1'] and \
                            opt_cargo is not None:
                        self.down_log.append({
                            'id': opt_cargo.id,
                            'time': self.clock,
                            'cnc': self.get_cnc_id(self.entity_dict['RGV'].posi, 1)
                        })
                    elif new_inst == rgv.RGV_modecode_rev['supply cargo 2'] and \
                            opt_cargo is not None:
                        self.down_log.append({
                            'id': opt_cargo.id,
                            'time': self.clock,
                            'cnc': self.get_cnc_id(self.entity_dict['RGV'].posi, 2)
                        })

            if name == 'CNC':
                for e in entity[1:]:
                    event, cargo = e.update()

        self.clock += 1
        return 0

    def simulate(self):
        for _ in range(self.total_time):
            flag = self.update()
            if flag == -1:
                print("ERROR at", self.clock)
                self.info()
                break

    def info(self):
        print("Clock: {}".format(self.clock))
        print("RGV:")
        print("\t{}".format(rgv.RGV_modecode[self.entity_dict['RGV'].status]))
        if self.entity_dict['RGV'].carry is not None:
            print("\t{}, {}".format(self.entity_dict['RGV'].carry.id,
                                    Cargo_modecode[
                                        self.entity_dict['RGV'].carry.status
                                    ]))
        for i, c in enumerate(self.entity_dict['CNC'][1:]):
            print("CNC {}:".format(i + 1))
            print("\t{}".format(cnc.CNC_modecode[c.status]))
            if c.proc is not None:
                print("\t{}, {}".format(c.proc.id,
                                        Cargo_modecode[
                                            c.proc.status
                                        ]))

        print("current cargo: {}".format(self.cargo_id))
        print()

    def final(self):
        print(self.entity_dict['RGV'].inst_list)
        print(self.up_log)
        print(self.down_log)

    # static method
    def get_cnc_id(self, posi, side):
        if side == 1:
            return posi * 2 - 1
        elif side == 2:
            return posi * 2

    def cnc_current(self, posi, side):
        if side == 1:
            cnc_id = posi * 2 - 1
        elif side == 2:
            cnc_id = posi * 2
        else:
            return -1

        return self.entity_dict['CNC'][cnc_id].proc

    def cnc_check(self, posi, side):
        if side == 1:
            cnc_id = posi * 2 - 1
        elif side == 2:
            cnc_id = posi * 2
        else:
            return -1

        return self.entity_dict['CNC'][cnc_id].status

    def cnc_supply(self, posi, side, cargo_t):
        if side == 1:
            cnc_id = posi * 2 - 1
        elif side == 2:
            cnc_id = posi * 2
        else:
            return -1

        self.entity_dict['CNC'][cnc_id].proc = cargo_t
        flag, _ = self.entity_dict['CNC'][cnc_id].inst(cnc.CNC_modecode_rev['processing'])
        return flag

    def cnc_consume(self, posi, side):
        if side == 1:
            cnc_id = posi * 2 - 1
        elif side == 2:
            cnc_id = posi * 2
        else:
            return -1

        tmp = self.entity_dict['CNC'][cnc_id].proc
        self.entity_dict['CNC'][cnc_id].proc = None
        self.entity_dict['CNC'][cnc_id].inst(cnc.CNC_modecode_rev['idle'])
        return tmp
