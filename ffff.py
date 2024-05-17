import pandas as pd
from Job import Job
import random
from Machine import Machine
import Individual

jobs_dict = {}
setw = set()


def main():
    read_file('psc.csv')
    print(Job.get_number_of_machines(jobs_dict))

    initial_population = generate_population(jobs_dict, 100)
    for i, chromosome in enumerate(initial_population):
        print(f"chromosome {i + 1}: {chromosome}")


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
            machine = Machine(machine_id, duration, None, 0)
        else:
            machine = Machine(machine_id, duration, pred, 0)

        setw.add(job_id)
        job.machine_dict.update({operation: machine})

        pred = machine

def generate_population(jobs, population_size):
    population = []

    def generate_chromosome():
        initial_chromosome = []
        for job in jobs.values():
            initial_chromosome.extend([job.id] * job.op_number)
        random.shuffle(initial_chromosome)
        return initial_chromosome

    for i in range(population_size):
        population.append(generate_chromosome())
    return population



if __name__ == '__main__':
    main()
