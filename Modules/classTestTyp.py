class TestTyp:
    """
    Represents all different test types

    Construction:

    >>> TestTyp(name, *pools)

    :param name: Name of the test type, for example the name of Experiment
    :type name: str

    :param pools: Pools belonging to the test type, mind the "*"
    :type pools: list[pool]

    """

    def __init__(self, name, *pools):
        """
        Creates instance of TestTyp

        """
        self.name = name
        # Name of the test type, for example the name of experiment
        self.pools = pools
        # list of pools belonging to the test type from which problems should be selected
