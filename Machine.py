from enum import Enum


class Machine:

    def __init__(self, id, duration, predecessor):
        self.id = id
        self.duration = duration
        self.predecessor = predecessor
        self.starting_time = None