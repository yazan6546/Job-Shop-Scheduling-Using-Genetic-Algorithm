from enum import Enum


class Machine:

    def __init__(self, id, duration, predecessor):
        self.id = id
        self.duration = duration
        self.remaining_time = duration
        self.predecessor = predecessor
        self.is_finished = False
        self.is_busy = False
        self.starting_time = None

    def decrement_remaining_time(self):

        if self.remaining_time == 1:
            self.is_finished = True
        else:
            self.remaining_time -= 1

    @staticmethod
    def increment_waiting_time(dict_machines_busy, dict_machines_waiting_time):

        for id, busy in dict_machines_busy:
            if not busy:
                dict_machines_waiting_time[id] += 1
