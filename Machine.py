from enum import Enum


class Machine:

    def __init__(self, id, duration, predecessor):
        self.id = id
        self.duration = duration
        self.remaining_time = duration
        self.waiting_time = 0
        self.predecessor = predecessor
        self.is_finished = False
        self.is_busy = False
        self.starting_time = None

    def decrement_remaining_time(self):

        if self.remaining_time == 0:
            self.is_finished = True
        else:
            self.remaining_time -= 1
