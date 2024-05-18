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

    def calculate_makespan(self, job_dict):
        # Initialize machine availability and job completion arrays

        set_id = Job.get_set_of_machines(job_dict)
        machine_availability = {}
        for machine_id in set_id:
            machine_availability[machine_id] = 0

        dictionary = {}

        # Process each operation in the chromosome
        for gene in self.chromosome:

            if gene in dictionary:
                dictionary[gene] += 1
            else:
                dictionary[gene] = 1

            job_id = gene
            op_number = dictionary[gene]
            machine = job_dict[job_id].machine_dict_op[op_number]

            # m2 = 3, m1 = 4
            # Calculate start time for the current operation
            job_dict[job_id].start_time = max(machine_availability[machine.id], job_dict[job_id].finish_time)

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

        self.calculate_makespan(jobs_dict)
        machine_gantt = Individual.initialize_dict(set_machines)
        for job in jobs_dict.values():
            machines = job.machine_dict_id

            for machine_id in set_machines:
                if machine_id in machines:
                    machine_gantt[machine_id].append(job)

        print(machine_gantt)

    @staticmethod
    def initialize_dict(set_machines):

        dictionary = {}
        for i in set_machines:
            dictionary[i] = []

        return dictionary
