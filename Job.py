class Job:

    def __init__(self, machine_dict_op, machine_dict_id, id, op_number):
        self.machine_dict_op = machine_dict_op
        self.machine_dict_id = machine_dict_id
        self.id = id
        self.op_number = op_number
        self.finish_time = 0

    def calculate_total_duration(self):
        total_duration = 0
        for machine in self.machine_dict_op.values():
            total_duration += machine.duration
            return total_duration

    @staticmethod
    def get_set_of_machines(jobs_dict):

        id_set = set()
        for job in jobs_dict.values():
            temp_list = [machine.id for machine in job.machine_dict_op.values()]
            id_set.update(set(temp_list))

        return id_set
