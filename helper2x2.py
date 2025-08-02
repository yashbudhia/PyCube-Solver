import random

def getScramble2x2(length=10):
    """
    Generate a random scramble for 2x2 cube.
    Use simpler moves to ensure the cube can be solved by current solver.
    
    Parameters
    ----------
    length : int, default=10
        Length of the scramble sequence.
        
    Returns
    -------
    scramble : string
        Random scramble sequence in format compatible with parseFormula.
    """
    # Use simpler moves that our solver can handle
    moves = ["R", "R'", "U", "U'", "F", "F'"]  # Removed 2x moves for now
    scramble = []
    last_move = ""
    
    for _ in range(length):
        move = random.choice(moves)
        # Avoid consecutive moves on same face
        while move[0] == last_move:
            move = random.choice(moves)
        scramble.append(move)
        last_move = move[0]
    
    # Return with spaces for parseFormula compatibility
    return " ".join(scramble)
