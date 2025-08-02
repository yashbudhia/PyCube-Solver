import random

def getScramble4x4(length=30):
    """
    Generate a random scramble sequence for a 4x4 cube.
    
    Parameters
    ----------
    length : int, default=30
        The number of moves in the scramble sequence.
        
    Returns
    -------
    scramble : string
        A space-separated string of cube moves.
    """
    # 4x4 moves include face turns and wide turns
    moves = [
        "R", "R'", "R2", "L", "L'", "L2",
        "U", "U'", "U2", "D", "D'", "D2", 
        "F", "F'", "F2", "B", "B'", "B2",
        "r", "r'", "r2", "l", "l'", "l2",
        "u", "u'", "u2", "d", "d'", "d2",
        "f", "f'", "f2", "b", "b'", "b2"
    ]
    
    # Opposite faces to avoid redundant moves
    opposite_faces = {
        'R': 'L', 'L': 'R',
        'U': 'D', 'D': 'U', 
        'F': 'B', 'B': 'F',
        'r': 'l', 'l': 'r',
        'u': 'd', 'd': 'u',
        'f': 'b', 'b': 'f'
    }
    
    scramble = []
    last_face = None
    
    for _ in range(length):
        available_moves = moves.copy()
        
        # Remove moves that would cancel with the last move
        if last_face:
            # Remove same face moves
            available_moves = [m for m in available_moves if not m.startswith(last_face)]
            # Remove opposite face moves
            if last_face in opposite_faces:
                opposite = opposite_faces[last_face]
                available_moves = [m for m in available_moves if not m.startswith(opposite)]
        
        move = random.choice(available_moves)
        scramble.append(move)
        last_face = move[0]  # Get the face letter
    
    return "".join(scramble)

def optimizeScramble4x4(scramble):
    """
    Basic optimization of a 4x4 scramble to remove redundant moves.
    
    Parameters
    ----------
    scramble : string
        The scramble sequence to optimize.
        
    Returns
    -------
    optimized : string
        The optimized scramble sequence.
    """
    moves = scramble.split()
    optimized = []
    
    i = 0
    while i < len(moves):
        current = moves[i]
        
        # Look ahead for consecutive moves on the same face
        consecutive = [current]
        j = i + 1
        while j < len(moves) and moves[j][0] == current[0]:
            consecutive.append(moves[j])
            j += 1
        
        # Combine consecutive moves
        if len(consecutive) == 1:
            optimized.append(current)
        else:
            # Calculate total rotation
            total_rotation = 0
            for move in consecutive:
                if move.endswith("'"):
                    total_rotation -= 1
                elif move.endswith("2"):
                    total_rotation += 2
                else:
                    total_rotation += 1
            
            # Normalize rotation
            total_rotation = total_rotation % 4
            
            # Convert back to move notation
            face = current[0]
            if total_rotation == 1:
                optimized.append(face)
            elif total_rotation == 2:
                optimized.append(face + "2")
            elif total_rotation == 3:
                optimized.append(face + "'")
            # total_rotation == 0 means no move needed
        
        i = j
    
    return " ".join(optimized)
