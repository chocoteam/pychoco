class Contradiction(Exception):
    """
    Raised inside a Python propagator callback when a domain filtering
    operation empties a variable's domain (i.e. signals a contradiction
    to the Choco solver, which will trigger backtracking).
    """
    pass
