import pandas as pd
import numpy as np
from Job import Job
import random
from Machine import Machine
from Individual import *

jobs_dict = {}
setw = set()


def main():
    read_file('psc.csv')
    run_algorithm()


def run_algorithm():
    initial_population = generate_population(jobs_dict, 10)
    #for i, chromosome in enumerate(initial_population):
        #print(f"chromosome {i + 1}: {chromosome.chromosome}")
        #print(chromosome.calculate_makespan(jobs_dict))

    fittest = min(initial_population, key=lambda individual: individual.calculate_makespan(jobs_dict))
    #print(fittest.calculate_makespan(jobs_dict))

    for _ in range(200):

        p1, p2 = select_parents(initial_population)
        offspring1, offspring2 = partially_mapped_crossover(p1, p2)
        # Mutation test

        if random.random() < 0.1:
            insertion_mutation(offspring1)

        if random.random() < 0.1:
            insertion_mutation(offspring2)

        discard_individuals(initial_population, offspring1, offspring2)

    # choose the individual with the highest fitness

    fittest = min(initial_population, key=lambda individual: individual.calculate_makespan(jobs_dict))
    #print(fittest.chromosome)
    #print(fittest.calculate_makespan(jobs_dict))
    Individual.create_gantt_chart(fittest,jobs_dict)


def read_file(file_name):
    file = pd.read_csv(file_name)

    for i in range(len(file)):
        temp_list = list(file.iloc[i])

        job_id = temp_list[0]
        operation = temp_list[1]
        machine_id = temp_list[2]
        duration = temp_list[3]

        if job_id not in setw:
            machine_dict_op = {}
            machine_dict_id = {}

            op_number = (file['job_id'] == job_id).sum()

            job = Job(machine_dict_op, machine_dict_id, job_id, op_number)
            jobs_dict.update({job.id: job})
            machine = Machine(machine_id, duration, None)
        else:
            machine = Machine(machine_id, duration, pred)

        setw.add(job_id)
        job.machine_dict_op.update({operation: machine})
        job.machine_dict_id.update({machine_id: machine})

        pred = machine


def get_occurrence_tuples(array):
    # Dictionary to keep track of occurrences
    occurrence_dict = {}
    # List to store the result tuples
    result = []

    # Iterate through the array
    for num in array:
        # Update the occurrence count
        if num in occurrence_dict:
            occurrence_dict[num] += 1
        else:
            occurrence_dict[num] = 1

        # Append the current number and its count to the result list
        result.append((num, occurrence_dict[num]))

    return result


def extract_numbers(tuple_list):
    result = []

    for num, _ in tuple_list:
        result.append(num)

    return result


def partially_mapped_crossover(A, B):
    A = get_occurrence_tuples(A.chromosome)
    B = get_occurrence_tuples(B.chromosome)
    point1 = random.randint(0, len(A) - 2)
    point2 = random.randint(point1 + 1, len(A) - 1)

    def find_offspring(p1, p2):

        offspring = [(0, 0) for _ in range(len(p1))]
        offspring[point1:point2] = p1[point1:point2]
        for i in np.concatenate([np.arange(0, point1), np.arange(point2, len(p1))]):
            current = p2[i]
            while current in p1[point1:point2]:
                current = p2[find_tuple_index(p1, current)]
            offspring[i] = current
        offspring = extract_numbers(offspring)
        return offspring

    offspring1 = find_offspring(A, B)
    offspring2 = find_offspring(B, A)
    return Individual(offspring1), Individual(offspring2)


def insertion_mutation(individual):
    index = random.randint(0, len(individual.chromosome) - 1)
    gene = individual.chromosome.pop(index)
    new_position = random.randint(0, len(individual.chromosome))
    individual.chromosome.insert(new_position, gene)
    return individual


def find_tuple_index(lst, target_tuple):
    for index, tup in enumerate(lst):
        if tup == target_tuple:
            return index
    return None


def generate_population(jobs, population_size):
    population = []

    def generate_chromosome():
        initial_chromosome = []
        for job in jobs.values():
            initial_chromosome.extend([job.id] * job.op_number)
        random.shuffle(initial_chromosome)
        return Individual(initial_chromosome)

    for i in range(population_size):
        population.append(generate_chromosome())
    return population


def select_parents(population):
    fitness = [1 / (chromosome.calculate_makespan(jobs_dict)) for chromosome in population]
    p1, p2 = random.choices(population, weights=fitness, k=2)

    # Ensure p1 and p2 are distinct, if not, reselect p2
    while p1 == p2:
        p2 = random.choices(population, weights=fitness, k=1)[0]

    return p1, p2


def discard_individuals(population, offspring1, offspring2):
   # makespan = [(chromosome.calculate_makespan(jobs_dict)) for chromosome in population]
   # p1, p2 = random.choices(population, weights=makespan, k=2)

   # print(p1.chromosome)
   # print(p2.chromosome)
    # Ensure p1 and p2 are distinct, if not, reselect p2
   # while p1 == p2:
  #      p2 = random.choices(population, weights=makespan, k=1)[0]

    #population.remove(p1)
   # population.remove(p2)

    population.append(offspring1)
    population.append(offspring2)


if __name__ == '__main__':
    main()
