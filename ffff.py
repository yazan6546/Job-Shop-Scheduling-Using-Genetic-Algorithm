import pandas as pd
import numpy as np
from Job import Job
import random
from Machine import Machine
import Individual

jobs_dict = {}
setw = set()


def main():
    read_file('psc.csv')

    initial_population = generate_population(jobs_dict, 5)
    for i, chromosome in enumerate(initial_population):
        print(f"chromosome {i + 1}: {chromosome.chromosome}")

    offspring1, offspring2 = partially_mapped_crossover(initial_population[0], initial_population[1])
    print(offspring1.chromosome)
    print(offspring1.calculate_makespan(jobs_dict))
    print(insertion_mutation(initial_population[0]).chromosome)


def read_file(file_name):
    file = pd.read_csv(file_name)

    for i in range(len(file)):
        temp_list = list(file.iloc[i])

        job_id = temp_list[0]
        operation = temp_list[1]
        machine_id = temp_list[2]
        duration = temp_list[3]

        if job_id not in setw:
            machine_dict = {}

            op_number = (file['job_id'] == job_id).sum()

            job = Job(machine_dict, job_id, op_number)
            jobs_dict.update({job.id: job})
            machine = Machine(machine_id, duration, None)
        else:
            machine = Machine(machine_id, duration, pred)

        setw.add(job_id)
        job.machine_dict.update({operation: machine})

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
    print(A)
    print(B)
    point1 = random.randint(0,len(A) - 2)
    point2 = random.randint(point1 + 1,len(A) - 1)
    print(point1)
    print(point2)
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
    return Individual.Individual(offspring1), Individual.Individual(offspring2)


def insertion_mutation(individual):
    index = random.randint(0,len(individual.chromosome) - 1)
    gene = individual.chromosome.pop(index)
    new_position = random.randint(0,len(individual.chromosome))
    individual.chromosome.insert(new_position,gene)
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
        return Individual.Individual(initial_chromosome)

    for i in range(population_size):
        population.append(generate_chromosome())
    return population


if __name__ == '__main__':
    main()
