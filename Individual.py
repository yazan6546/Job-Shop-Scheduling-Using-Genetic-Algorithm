import random
from Machine import *
from Job import *


class Individual:
    """
    Class representing individual in population
    """

    def __init__(self, chromosome):
        self.chromosome = chromosome

    @classmethod
    def mutated_genes(self):
        """
        create random genes for mutation
        """
        global GENES
        gene = random.choice(GENES)
        return gene

    @classmethod
    def create_gnome(self):
        """
        create chromosome or string of genes
        """
        global TARGET
        gnome_len = len(TARGET)
        return [self.mutated_genes() for _ in range(gnome_len)]

    def mate(self, par2):
        """
        Perform mating and produce new offspring
        """

        # chromosome for offspring
        child_chromosome = []
        for gp1, gp2 in zip(self.chromosome, par2.chromosome):

            # random probability
            prob = random.random()

            # if prob is less than 0.45, insert gene
            # from parent 1
            if prob < 0.45:
                child_chromosome.append(gp1)

                # if prob is between 0.45 and 0.90, insert
            # gene from parent 2
            elif prob < 0.90:
                child_chromosome.append(gp2)

                # otherwise insert random gene(mutate),
            # for maintaining diversity
            else:
                child_chromosome.append(self.mutated_genes())

                # create new Individual(offspring) using
        # generated chromosome for offspring
        return Individual(child_chromosome)

    def calculate_makespan(self, num_jobs, num_machines, job_dict):
        # Initialize machine availability and job completion arrays
        machine_availability = [0] * num_machines
        job_completion = [0] * num_jobs

        dictionary = {}

        # Process each operation in the chromosome
        for gene in self.chromosome:

            if gene not in dictionary:
                dictionary[gene] += 1
            else:
                dictionary[gene] = 1

            job_id = gene
            op_number = dictionary[gene]
            machine = job_dict[job_id].machine_dict[op_number]

            # Calculate start time for the current operation
            start_time = max(machine_availability[machine.id], job_dict[job_id].finish_time)

            # Calculate finish time for the current operation
            finish_time = start_time + machine.duration

            # Update machine availability and job completion times
            machine_availability[machine.id] = finish_time
            job_dict[job_id].finish_time = finish_time

        # The makespan is the maximum job completion time
        makespan = max(job_dict.values(), key=lambda job: job.finish_time)
        return makespan

    def handle_chromosome(self, jobs_dict, dictionary, list_machines, dict_machines_busy, time):

        for gene in self.chromosome:
            if gene not in dictionary:
                dictionary[gene] += 1
            else:
                dictionary[gene] = 1

            job = jobs_dict[gene]
            op_number = dictionary[gene]
            machine = jobs_dict[gene].machine_dict[op_number]

            if (not dict_machines_busy[machine.id] and
                    machine.predecessor is None or
                    machine.predecessor.is_finished and
                    not machine.is_finished):
                list_machines[machine.id].append(job)
                dict_machines_busy[machine.id] = True
                machine.is_busy = True
                machine.starting_time = time

            if machine.duration == 0:
                dict_machines_busy[machine] = False
                machine.is_finished = True

    def scheduling(self, jobs_dict, set_id):

        number_machines = len(set_id)
        time = 0
        list_machines = Individual.initialize_list(number_machines)
        dict_machines_busy = {}

        for machine_id in set_id:
            dict_machines_busy[machine_id] = False

        dict_machines_waiting_time = {}

        for machine_id in set_id:
            dict_machines_waiting_time[machine_id] = 0

        dict = {}  # to handle the number of occurrences

        while not Individual.is_finished(jobs_dict):  # terminate when all has finished
            Job.decrement_working_machines(jobs_dict)
            self.handle_chromosome(jobs_dict, dict, list_machines, dict_machines_busy, time)
            time += 1

    @staticmethod
    def is_finished(jobs_dict):
        return all(all(machine.is_finished() for machine in job.machine_dict.values()) for job in jobs_dict.values())

    @staticmethod
    def initialize_list(number_machines):

        list_main = []
        for i in range(number_machines):
            list_main.append([])

        return list_main
