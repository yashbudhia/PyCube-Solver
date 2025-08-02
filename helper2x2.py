import random

def getScramble2x2(length=10):
    """
    Generate a random scramble for 2x2 cube.
    
    Parameters
    ----------
    length : int, default=10
        Length of the scramble sequence.
        
    Returns
    -------
    scramble : string
        Random scramble sequence.
    """
    moves = ["R", "R'", "R2", "U", "U'", "U2", "F", "F'", "F2"]
    scramble = []
    last_move = ""
    
    for _ in range(length):
        move = random.choice(moves)
        # Avoid consecutive moves on same face
        while move[0] == last_move:
            move = random.choice(moves)
        scramble.append(move)
        last_move = move[0]
    
    return " ".join(scramble)
