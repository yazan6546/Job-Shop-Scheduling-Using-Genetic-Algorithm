# Ahmad Qaimari-1210190
# Yazan AboEloun-1210145
import pandas as pd
import random
import numpy as np
from Individual import *

# Dictionary to keep track of all Jobs in this problem
jobs_dict = {}

# Set to keep track of operation numbers when reading from the file
setw = set()


def main():
    read_file('psc.csv')
    run_algorithm()


def run_algorithm():
    initial_population = generate_population(jobs_dict, 10)
    # for i, chromosome in enumerate(initial_population):
    # print(f"chromosome {i + 1}: {chromosome.chromosome}")
    # print(chromosome.calculate_makespan(jobs_dict))

    fittest_initial = min(initial_population, key=lambda individual: individual.calculate_makespan(jobs_dict))
    print(fittest_initial.calculate_makespan(jobs_dict))
    Individual.create_gantt_chart(fittest_initial, jobs_dict)
    for _ in range(50):

        p1, p2 = select_parents(initial_population)
        offspring1, offspring2 = partially_mapped_crossover(p1, p2)
        # Mutation test

        if random.random() < 0.1:
            insertion_mutation(offspring1)

        if random.random() < 0.1:
            insertion_mutation(offspring2)

        initial_population.append(offspring1)
        initial_population.append(offspring2)

    # choose the individual with the highest fitness

    fittest = min(initial_population, key=lambda individual: individual.calculate_makespan(jobs_dict))
    print(fittest.calculate_makespan(jobs_dict))
    Individual.create_gantt_chart(fittest, jobs_dict)


def read_file(file_name):
    """
    Read a CSV file containing job and machine descriptions and update the job and machine dictionaries in place.

    Parameters:
    ----------
    file_name : str
        The name of the CSV file to read.

    Returns:
    -------
    None
    """

    file = pd.read_csv(file_name)

    # Traverse all rows in the file
    for i in range(len(file)):

        # Get row i
        temp_list = list(file.iloc[i])

        # Read the corresponding columns in row i
        job_id = temp_list[0]
        operation = temp_list[1]
        machine_id = temp_list[2]
        duration = temp_list[3]

        # Test if the Job_id has been seen before, of not, then we need to create new job and machine objects
        if job_id not in setw:
            # Initialize machine dictionaries one with key : id, the other with key : operation number
            machine_dict_op = {}
            machine_dict_id = {}

            # Get the number of operations for a given job id
            op_number = (file['job_id'] == job_id).sum()

            # Create a new job object and add to the main dictionary
            job = Job(machine_dict_op, machine_dict_id, job_id, op_number)
            jobs_dict.update({job.id: job})
            machine = Machine(machine_id, duration, None)
        else:
            machine = Machine(machine_id, duration, pred)

        setw.add(job_id)

        # add the machine object to machines dictionaries
        job.machine_dict_op.update({operation: machine})
        job.machine_dict_id.update({machine_id: machine})

        pred = machine


def get_occurrence_tuples(array):
    """
    Generate tuples of elements and their current occurrences as encountered in the array.

    Parameters:
    ----------
    array : list
        A list of elements.

    Returns:
    -------
    list of tuples
        A list where each tuple contains an element from the array and its count at that point in the iteration.
    """

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


def partially_mapped_crossover(A, B):
    """
    Perform partially mapped crossover (PMX) on two parent individuals to produce two offspring.

    Parameters:
    ----------
    A : Individual
        The first parent individual.
    B : Individual
        The second parent individual.

    Returns:
    -------
    tuple of Individual
        A tuple containing two offspring individuals resulting from the crossover.
    """
    # Generate occurrence tuples for both parents' chromosomes
    A = get_occurrence_tuples(A.chromosome)
    B = get_occurrence_tuples(B.chromosome)

    # Select two crossover points
    point1 = random.randint(0, len(A) - 2)
    point2 = random.randint(point1 + 1, len(A) - 1)

    def find_offspring(p1, p2):

        # Initialize offspring with placeholders
        offspring = [(0, 0) for _ in range(len(p1))]

        # Copy the segment between the crossover points from p1 to offspring
        offspring[point1:point2] = p1[point1:point2]

        # Fill in the rest of the offspring's chromosome
        for i in np.concatenate([np.arange(0, point1), np.arange(point2, len(p1))]):
            current = p2[i]
            while current in p1[point1:point2]:
                current = p2[find_tuple_index(p1, current)]
            offspring[i] = current

        # Extract only the first elements of the tuples to form the chromosome
        offspring = [num[0] for num in offspring]

        return offspring

    # Create the two offspring by applying the PMX
    offspring1 = find_offspring(A, B)
    offspring2 = find_offspring(B, A)

    # Return the offspring as new Individual objects
    return Individual(offspring1), Individual(offspring2)


def insertion_mutation(individual):
    """
    Perform insertion mutation on the given individual.

    Parameters:
    ----------
    individual : Individual
        The individual to undergo mutation.

    Returns:
    -------
    Individual
        The mutated individual.
    """
    # Select a random index from the chromosome
    index = random.randint(0, len(individual.chromosome) - 1)

    # Remove the gene at the selected index and store it
    gene = individual.chromosome.pop(index)

    # Choose a new random position for the gene and insert it
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


if __name__ == '__main__':
    main()
