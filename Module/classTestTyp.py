class TestTyp:
    """Repräsentiert alle verschiedenen TestTypen
    
    Konstruktion:
        
        >>> TestTyp(name, *pools)
        
        * name:
            Name des TestTyps, z.B. Versuchsnummer
            
        * *pools:
            Liste von gewuenschten Pools im TestTyp.
            Liste mit Praefix "*" angeben (so wird diese als Aneinandereihung mit 
                                           Kommata wiedergegeben)"""
            
    def __init__(self, name, *pools):
        "Instanziert einen TestTyp"
        self.name = name
        """Name des Testtyps, wahrscheinlich der Name des Versuches, z.B. V21"""
        self.pools = pools
        """Liste von Pools, aus denen Aufgaben gezogen werden sollen"""

