class World:
    def __init__(self, total_time):
        # init all objects
        self.entity_list = []
        self.entity_list.append()

        # clock
        self.clock = 0
        self.total_time = total_time

        # logging
        self.count = 0
        self.up_log = [{'id': 1, 'time': 0}]
        self.down_log = []

    def update(self):
        for entity in self.entity_list:
            event = entity.update()
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
