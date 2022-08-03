class TestTyp:
    """Represents all different test types

    Construction:

        >>> TestTyp(name, *pools)

        * name:
            Name of the test type, for example the name of Experiment

        * *pools:
            list of pools belonging to the test type
            start with prefix "*" in order to have an enumeration separated by ","
    """

    def __init__(self, name, *pools):
        "Creates instance of TestTyp"
        self.name = name
        """Name of the test type, for example the name of experiment"""
        self.pools = pools
        """list of pools belonging to the test type from which problems should be selected"""
