class Job:
    """
    Class representing a job in a scheduling problem.

    Attributes:
    ----------
    machine_dict_op : dict
        A dictionary where keys are operation identifiers and values are machine objects for those operations.
    machine_dict_id : dict
        A dictionary where keys are machine identifiers and values are operation objects for those machines.
    id : int
        The unique identifier for the job.
    op_number : int
        The operation number for the job.
    finish_time : int
        The finish time for the job. Initialized to 0.
    """

    def __init__(self, machine_dict_op, machine_dict_id, id, op_number):
        """
        Initialize a job with given machine operation dictionary, machine ID dictionary, job ID, and operation number.

        Parameters:
        ----------
        machine_dict_op : dict
            A dictionary where keys are operation numbers and values are machine objects.
        machine_dict_id : dict
            A dictionary where keys are machine IDs and values are operation objects.
        id : int
            The unique identifier for the job.
        op_number : int
            The operation number for the job.
        """
        self.machine_dict_op = machine_dict_op
        self.machine_dict_id = machine_dict_id
        self.id = id
        self.op_number = op_number
        self.finish_time = 0

    def calculate_total_duration(self):
        """
        Calculate the total duration of all operations in the job.

        Returns:
        -------
        int
            The total duration of all operations.
        """
        total_duration = 0
        for machine in self.machine_dict_op.values():
            total_duration += machine.duration
        return total_duration

    @staticmethod
    def get_set_of_machines(jobs_dict):
        """
        Get a set of all machine identifiers used in a dictionary of jobs.

        Parameters:
        ----------
        jobs_dict : dict
            A dictionary where keys are job identifiers and values are Job objects.

        Returns:
        -------
        set
            A set of all machine identifiers used in the jobs.
        """
        id_set = set()

        for job in jobs_dict.values():

            # create a list of all IDs in a machine needed by a particular job
            temp_list = [machine.id for machine in job.machine_dict_op.values()]

            # remove duplicates
            id_set.update(set(temp_list))

        return id_set
