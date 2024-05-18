class Job:


    def __init__(self, machine_dict, id, op_number):
        self.machine_dict = machine_dict
        self.id = id
        self.op_number = op_number

    def calculate_total_duration(self):
        total_duration = 0
        for machine in self.machine_dict.values():
            total_duration += machine.duration
            return total_duration

    @staticmethod
    def get_number_of_machines(jobs_dict):

        id_set = set()
        for job in jobs_dict.values():
            temp_list = [machine.id for machine in job.machine_dict.values()]
            id_set.update(set(temp_list))

        return len(id_set)

    @staticmethod
    def decrement_working_machines(jobs_dict, list_waiting):
        for job in jobs_dict.values():
            machines = job.machine_dict.values()

            for machine in machines:
                if machine.is_busy:
                    machine.decrement_remaining_time()