import rgv
import cnc


class World:
    def __init__(self, alg, total_time):
        # tricky
        self.cnc_api = {
            'status': self.cnc_check,
            'supply': self.cnc_supply,
            'consume': self.cnc_consume
        }

        self.alg = alg

        # init all objects
        self.entity_dict = dict()
        self.entity_dict['RGV'] = rgv.RGV(rgv.RGV_param, self.cnc_api)
        self.entity_dict['CNC'] = [
            -1,
            cnc.CNC(cnc.CNC_proctime_1),
            cnc.CNC(cnc.CNC_proctime_1),
            cnc.CNC(cnc.CNC_proctime_1),
            cnc.CNC(cnc.CNC_proctime_1),
            cnc.CNC(cnc.CNC_proctime_1),
            cnc.CNC(cnc.CNC_proctime_1),
            cnc.CNC(cnc.CNC_proctime_1),
            cnc.CNC(cnc.CNC_proctime_1)
        ]

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
                event, cargo = entity.update()
                if event is not None:
                    # main processions
                    if event != 0:
                        print(rgv.RGV_modecode[event])
                        self.info()

                    if event == rgv.RGV_modecode_rev['supply cargo 1'] or \
                            event == rgv.RGV_modecode_rev['supply cargo 2']:
                        self.up_log.append({
                            'id': cargo,
                            'time': self.clock
                        })
                    elif event == rgv.RGV_modecode_rev['consume cargo 1'] or \
                            event == rgv.RGV_modecode_rev['consume cargo 2']:
                        self.down_log.append({
                            'id': cargo,
                            'time': self.clock
                        })

                    new_inst = self.alg(self.entity_dict)
                    if new_inst == rgv.RGV_modecode_rev['supply cargo 1'] or \
                            new_inst == rgv.RGV_modecode_rev['supply cargo 2']:
                        self.cargo_id += 1
                    flag = self.entity_dict['RGV'].inst(new_inst, self.cargo_id)
                    if flag == -1:
                        return -1

            if name == 'CNC':
                for e in entity[1:]:
                    event, cargo = e.update()
                    if event is not None:
                        print(rgv.RGV_modecode[event])

        self.clock += 1
        return 0

    def simulate(self):
        for _ in range(self.total_time):
            flag = self.update()
            if flag == -1:
                print("Error", self.clock)
                break

    def info(self):
        print("RGV:")
        print("\t{}".format(rgv.RGV_modecode[self.entity_dict['RGV'].status]))
        print("\t{}".format(self.entity_dict['RGV'].carry_id))
        for i, c in enumerate(self.entity_dict['CNC'][1:]):
            print("CNC {}:".format(i))
            print("\t{}".format(cnc.CNC_modecode[c.status]))
            print("\t{}".format(c.proc_id))

        print("current cargo: {}".format(self.cargo_id))

    def final(self):
        print(self.up_log)
        print(self.down_log)

    # static method
    def cnc_check(self, posi, side):
        if side == 1:
            cnc_id = posi * 2 - 1
        elif side == 2:
            cnc_id = posi * 2
        else:
            return -1

        return self.entity_dict['CNC'][cnc_id].proc_id

    def cnc_supply(self, posi, side, cid):
        if side == 1:
            cnc_id = posi * 2 - 1
        elif side == 2:
            cnc_id = posi * 2
        else:
            return -1

        self.entity_dict['CNC'][cnc_id].proc_id = cid
        self.entity_dict['CNC'][cnc_id].inst(cnc.CNC_modecode_rev['processing'])
        return 0

    def cnc_consume(self, posi, side):
        if side == 1:
            cnc_id = posi * 2 - 1
        elif side == 2:
            cnc_id = posi * 2
        else:
            return -1

        self.entity_dict['CNC'][cnc_id].proc_id = 0
        self.entity_dict['CNC'][cnc_id].inst(cnc.CNC_modecode_rev['idle'])
        return 0
