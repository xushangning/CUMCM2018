Cargo_modecode = {
    0: 'raw',
    1: 'half',
    2: 'ready',
    3: 'done'
}

Cargo_modecode_rev = {
    'raw': 0,
    'half': 1,
    'ready': 2,
    'done': 3
}

conveyer = {
    'raw conveyer': 0,
    'product conveyer': 1
}


class Cargo:
    def __init__(self, cid):
        self.id = cid
        self.status = Cargo_modecode_rev['raw']
        self.conveyer = conveyer['raw conveyer']
