from enum import Enum


class Machine:

    def __init__(self, id, duration, predecessor):
        self.id = id
        self.duration = duration
        self.predecessor = predecessor
        self.starting_time = None
        

    @staticmethod
    def increment_waiting_time(dict_machines_busy, dict_machines_waiting_time):

        for id, busy in dict_machines_busy:
            if not busy:
                dict_machines_waiting_time[id] += 1
