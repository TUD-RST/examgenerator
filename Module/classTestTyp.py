class TestTyp:
    def __init__(self, name, *pools):
        self.name = name
        """Name des Testtyps, wahrscheinlich der Name des Versuches, z.B. V21"""
        self.pools = pools
        """Liste von Pools, aus denen Aufgaben gezogen werden sollen"""

