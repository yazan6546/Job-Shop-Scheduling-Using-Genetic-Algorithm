import random
from Machine import *
from Job import *
import matplotlib.pyplot as plt


class Individual:
    """
    Class representing individual in population
    """

    def __init__(self, chromosome):
        self.chromosome = chromosome

    def calculate_makespan(self, job_dict):
        # Initialize machine availability and job completion arrays

        set_id = Job.get_set_of_machines(job_dict)
        machine_availability = {}
        for machine_id in set_id:
            machine_availability[machine_id] = 0

        # Job Id -> Job object
        for job in job_dict.values():
            job.start_time = 0
            job.finish_time = 0

        dictionary = {}

        # Process each operation in the chromosome
        for gene in self.chromosome:

            if gene in dictionary:
                dictionary[gene] += 1
            else:
                dictionary[gene] = 1

            job_id = gene
            op_number = dictionary[gene]
            # returns machine object for a specific operation of a particular job
            machine = job_dict[job_id].machine_dict_op[op_number]

            # m2 = 3, m1 = 4
            # Calculate start time for the current operation
            job_dict[job_id].start_time = max(machine_availability[machine.id], job_dict[job_id].finish_time)
            machine.starting_time = job_dict[job_id].start_time

            # Calculate finish time for the current operation
            finish_time = job_dict[job_id].start_time + machine.duration

            # Update machine availability and job completion times
            machine_availability[machine.id] = finish_time
            job_dict[job_id].finish_time = finish_time

        # The makespan is the maximum job completion time
        makespan = max(job_dict.values(), key=lambda job: job.finish_time)
        return makespan.finish_time

    def create_gantt_chart(self, jobs_dict):
        set_machines = Job.get_set_of_machines(jobs_dict)
        makespan = self.calculate_makespan(jobs_dict)
        machine_gantt = Individual.initialize_dict(set_machines)
        for job in jobs_dict.values():
            machines = job.machine_dict_id
            for machine_id in set_machines:
                if machine_id in machines:
                    machine_gantt[machine_id].append(job)
        fig, ax = plt.subplots()
        for index, machine_id in enumerate(machine_gantt):
            ypos = index * 10
            for job in machine_gantt[machine_id]:
                op_start = job.machine_dict_id[machine_id].starting_time
                op_finish = op_start + job.machine_dict_id[machine_id].duration
                ax.broken_barh([(op_start, job.machine_dict_id[machine_id].duration)], (ypos, 8), facecolors='skyblue',
                               edgecolors='black', linewidth=1)
                ax.text(
                    (op_start + op_finish) / 2,
                    ypos + 4,
                    f'J {job.id}',
                    ha='center',
                    va='center',
                    transform=ax.transData,
                    fontsize=10
                )
        num_ticks = 10
        interval = makespan / num_ticks
        interval = round(interval)
        ax.set_ylim(0, len(set_machines) * 10)
        ax.set_xlim(0, makespan)
        x_ticks = list(range(0, int(makespan) + 1, interval))
        x_ticks.pop()
        x_ticks.append(int(makespan))
        ax.set_xticks(x_ticks)
        ax.set_yticks([i * 10 + 4 for i in range(len(set_machines))])
        ax.set_xlabel('Time')
        ytick_labels = [f'Machine {machine_id}' for machine_id in set_machines]
        ax.set_yticklabels(ytick_labels)
        ax.set_ylabel('Machines')
        plt.title('Gantt Chart')
        plt.show()

    @staticmethod
    def initialize_dict(set_machines):

        dictionary = {}
        for i in set_machines:
            dictionary[i] = []

        return dictionary
