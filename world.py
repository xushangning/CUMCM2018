import rgv
import cnc


class World:
    def __init__(self, total_time):
        # tricky
        self.cnc_api = {
            'status': self.cnc_check,
            'supply': self.cnc_supply,
            'consume': self.cnc_consume
        }

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
        self.count = 0
        self.up_log = [{'id': 1, 'time': 0}]
        self.down_log = []

    def update(self):
        for name, entities in self.entity_dict:
            for entity in entities:
                event, cargo = entity.update()
                if event:
                    pass

        self.clock += 1

    def simulate(self):
        for _ in range(self.total_time):
            self.update()

    def info(self):
        print(self.up_log)
        print(self.down_log)
        print(self.count)

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
        return 0
