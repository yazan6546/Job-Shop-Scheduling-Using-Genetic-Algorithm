from enum import Enum


class Machine:

    def __init__(self, id, duration):
        self.id = id
        self.duration = duration
        self.starting_time = None
