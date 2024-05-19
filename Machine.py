
class Machine:

    def __init__(self, id, duration,predecessor):
        self.id = id
        self.duration = duration
        self.starting_time = None
        self.predecessor = predecessor
