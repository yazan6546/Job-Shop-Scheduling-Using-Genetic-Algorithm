from enum import Enum


class Status(Enum):
    WAITING = 0
    BUSY = 1
    FINISHED = 2


class Machine:

    def __init__(self, id, duration, predecessor, status):
        self.id = id
        self.duration = duration
        self.waiting_time = 0
        self.predecessor = predecessor
        self.status = status

    def is_finished(self):
        return self.status == Status.FINISHED