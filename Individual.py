import random
import Machine


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

    def cal_fitness(self):
        """
        Calculate fitness score, it is the number of
        characters in string which differ from target
        string.
        """
        global TARGET
        fitness = 0
        for gs, gt in zip(self.chromosome, TARGET):
            if gs != gt:
                fitness += 1
        return fitness

    def handle_chromosome(self, jobs_dict, mapping, dictionary):

        for gene in self.chromosome:
            if gene in dictionary:
                dictionary[gene] = dictionary[gene] + 1
            else:
                dictionary[gene] = 1

            op_number = dictionary[gene]
            machine = jobs_dict[gene].machine_dict[op_number]

            if (machine.status != Machine.Status.BUSY and
                machine.predecessor is None or
                machine.predecessor.status == Machine.Status.FINISHED):

                ############




    def scheduling(self, jobs_dict, mapping):

        dict = {}  # to handle the number of occurrences
        while not Individual.is_finished(jobs_dict):
            self.handle_chromosome(jobs_dict, mapping, dict)

    @staticmethod
    def is_finished(jobs_dict):
        return all(all(machine.is_finished() for machine in job.machine_dict.values()) for job in jobs_dict.values())


