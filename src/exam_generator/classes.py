"""
This module contains all classes relevant for the exam-generator.
"""

import random
import re

from .customExceptions import *
from .funcs import errorInfo


class Pool:
    """
    Represents each pool with its corresponding problems.

    Construction:

    >>> Pool(name, file_names_tex)

    :param name: Name of the pool for example: A1, CV21, DV07
    :type name: str

    :param pool_files: All Problem-Solution-file names of the pool
    :type pool_files: list[str]
    """

    def __init__(self, name, pool_files):
        """
        Creates new pool instance
        """

        self.name = name

        self.stack_available = []

        # [(filename_problem, filename_solution)]; problems that can be chosen from

        self.stack_pulled = []

        # [(filename_problem, filename_solution)]; selected problems for corresponding group

        self.stack_storage = []

        # [(filename_problem, filename_solution)]; problems which were pulled by last group

        # Creates a list with all problems of required pool
        problem_regex = re.compile(f"^problem_\\d+\\.tex$")
        file_names_pool_problems = [
            file for file in pool_files if re.match(problem_regex, file) is not None
        ]

        # Checks if problem + solution exists
        if len(file_names_pool_problems) == 0:
            raise MissingFileError(
                f"{errorInfo()} There is no problems available in Pool {self.name}. \
                Please ensure there is problem/ solution data for every used pool."
            )

        # Searches solution for problem
        for file in file_names_pool_problems:
            file_solution = file.replace("problem", "solution")

            # Adds problem and solution to stack
            if file_solution in pool_files:
                self.stack_available.append((file, file_solution))

            else:
                raise MissingFileError(
                    f"{errorInfo()} File {file_solution} does not exist. \
                    Please make sure that all your problem files have a corresponding solution file."
                )

    def pull(self):
        """
        Pulls a random problem + solution from the pool

        :return: prob_sol
        :rtype: tuple(str, str)
        """
        if len(self.stack_available) == 0:
            # Stack with available problems is exhausted
            # Storage stack is new available stack

            if len(self.stack_storage) > 0:
                self.stack_available = self.stack_storage
                self.stack_storage = []
            else:
                raise CompilingError(
                    f"{errorInfo()} Pool {self.name} is exhausted, problems might repeat within the group. \
                    Please ensure that your problem/ solution data size is sufficient."
                )
        # Random selection of problems/solution pairs
        prob_sol = self.stack_available.pop(
            random.randint(0, len(self.stack_available) - 1)
        )
        self.stack_pulled.append(prob_sol)

        return prob_sol

    def discard(self):
        """
        Discards all pulled problems to the discard pile
        """
        self.stack_storage.extend(self.stack_pulled)
        self.stack_pulled = []


class TestType:
    """
    Represents all different test types

    Construction:

    >>> TestType(name, *pools)

    :param name: Name of the test type, for example the name of Experiment
    :type name: str

    :param pools: Pools belonging to the test type, mind the "*"
    :type pools: list[pool]

    """

    def __init__(self, name, *pools):
        """
        Creates instance of TestType

        """
        self.name = name
        # Name of the test type, for example the name of experiment
        self.pools = pools
        # list of pools belonging to the test type from which problems should be selected
