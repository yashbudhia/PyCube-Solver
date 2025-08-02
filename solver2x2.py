from cube2x2 import Cube2x2
import random

class Solver2x2:
    """
    A 2x2 solver using the Ortega method, which involves three main steps:
    1. Build the first face (White).
    2. Orient the last layer (OLL).
    3. Permute the last layer (PLL).
    """
    
    def __init__(self, cube):
        self.cube = Cube2x2(faces=cube.getFaces())
        self.moves = []
        
        # OLL Algorithms (Top face is Yellow, Face 5)
        # The key is the pattern of yellow stickers on the top face, read from top-left.
        self.oll_algorithms = {
            (1, 1, 1, 1): "",  # Solved
            (0, 0, 0, 0): "R U R' U R U2 R'",
            (1, 0, 1, 0): "F R U R' U' F'",
            (0, 1, 0, 1): "F R U R' U' F'",
            (1, 1, 0, 0): "R2 U2 R U2 R2",
            (1, 0, 0, 1): "R U2 R' U' R U' R'",
            (0, 1, 1, 0): "R U2 R' U' R U' R'",
            (1, 0, 0, 0): "R U R' U R U2 R'",
        }

        # PLL Algorithms
        self.pll_algorithms = {
            "Adjacent": "R' U R' U2 R U' R' U2 R2",
            "Diagonal": "F R U' R' U' R U R' F' R U R' U' R' F R F'",
        }

    def solveCube(self, optimize=True):
        """Solve the 2x2 cube using the Ortega method."""
        self.moves = []
        if self._is_solved():
            return
            
        self._solve_first_face()
        self._orient_last_layer()
        self._permute_last_layer()
        
        # Final alignment
        for _ in range(4):
            if self._is_solved():
                break
            self._apply_move("U")

    def _apply_move(self, move_str):
        """Helper to apply a move or algorithm and record it."""
        if move_str:
            self.cube.doMoves(move_str)
            self.moves.append(move_str)

    def _solve_first_face(self):
        """
        Solves the first (white) face by finding the white corner that belongs
        at the bottom-front-right position and placing it correctly. Then,
        it solves the other three white corners relative to the first one.
        """
        # This is a more structured, albeit simple, way to solve the first face.
        # It's more reliable than random moves.

        # Goal: Get the White-Blue-Red corner to the DFR position (face 4, pos 1,1)
        # This is a simplification; a full implementation would be more complex.
        
        # A simple search to place a specific white piece (e.g., White-Blue-Red)
        # and then solve the rest of the layer. This is still hard.
        # Let's try a more reliable brute-force for just the first layer.
        
        solution = self._search_for_first_layer()
        if solution:
            for move in solution:
                self._apply_move(move)

    def _search_for_first_layer(self):
        """Performs a breadth-first search to find a solution for the first layer."""
        from collections import deque
        
        q = deque([([], self.cube.getFaces())])
        visited = {self.cube.getFacesAsTuple()}

        while q:
            moves, current_faces_list = q.popleft()
            
            temp_cube = Cube2x2(faces=current_faces_list)
            if self._is_first_face_solved(cube_obj=temp_cube):
                return moves

            if len(moves) >= 11: # Limit search depth for performance
                continue

            for move in ["R", "R'", "R2", "U", "U'", "U2", "F", "F'", "F2"]:
                next_cube = Cube2x2(faces=current_faces_list)
                next_cube.doMoves(move)
                next_faces_tuple = next_cube.getFacesAsTuple()

                if next_faces_tuple not in visited:
                    visited.add(next_faces_tuple)
                    new_moves = moves + [move]
                    q.append((new_moves, next_cube.getFaces()))
        return None

    def _orient_last_layer(self):
        """OLL step: Orient all yellow stickers to face up."""
        if self._is_oll_solved():
            return

        # Try to find a matching case by rotating the top layer
        for _ in range(4):
            top_face_pattern = self._get_oll_pattern()
            if top_face_pattern in self.oll_algorithms:
                alg = self.oll_algorithms[top_face_pattern]
                self._apply_move(alg)
                # Now OLL should be solved, we might just need to align.
                # The final alignment is handled by PLL and the final step.
                return
            self._apply_move("U")

        # If we get here, no OLL case was matched. This can happen if the
        # first face was not solved correctly. Apply a default alg to
        # change the state and hope for the best in the next stages.
        self._apply_move("R U R' U R U2 R'")

    def _permute_last_layer(self):
        """PLL step: Permute the top layer corners."""
        for _ in range(5):
            if self._is_pll_solved():
                return
            
            pll_case = self._get_pll_case()
            if pll_case in self.pll_algorithms:
                self._apply_move(self.pll_algorithms[pll_case])
                # Align after PLL
                for _ in range(4):
                    if self._is_pll_solved():
                        break
                    self._apply_move("U")
                return
            
            self._apply_move("U")

    def _is_first_face_solved(self, cube_obj=None):
        """Check if the white face is solved and the side colors match."""
        cube = cube_obj if cube_obj else self.cube
        faces = cube.getFaces()
        # Check if white face is all white
        if not all(sticker == 'W' for sticker in faces[4][0] + faces[4][1]):
            return False
        # Check if the side colors of the first layer form solid bars
        if not (faces[0][1][0] == faces[0][1][1] and
                faces[1][1][0] == faces[1][1][1] and
                faces[2][1][0] == faces[2][1][1] and
                faces[3][1][0] == faces[3][1][1]):
            return False
        return True

    def _get_oll_pattern(self):
        """Get the orientation pattern of the top (yellow) face."""
        top_face = self.cube.getFaces()[5]
        # Pattern is read from top-left, top-right, bottom-left, bottom-right
        return (
            1 if top_face[0][0] == 'Y' else 0,
            1 if top_face[0][1] == 'Y' else 0,
            1 if top_face[1][0] == 'Y' else 0,
            1 if top_face[1][1] == 'Y' else 0,
        )

    def _is_oll_solved(self):
        """Check if all yellow stickers are on the top face."""
        return all(sticker == 'Y' for row in self.cube.getFaces()[5] for sticker in row)

    def _get_pll_case(self):
        """Determine the PLL case by checking for 'headlights'."""
        faces = self.cube.getFaces()
        # Check for a solved bar on any of the four side faces' top layer
        if faces[0][0][0] == faces[0][0][1]: # Front
            return "Adjacent"
        if faces[1][0][0] == faces[1][0][1]: # Right
            return "Adjacent"
        if faces[2][0][0] == faces[2][0][1]: # Back
            return "Adjacent"
        if faces[3][0][0] == faces[3][0][1]: # Left
            return "Adjacent"
        return "Diagonal"

    def _is_pll_solved(self):
        """Check if the top layer corners are permuted correctly."""
        faces = self.cube.getFaces()
        return all(faces[i][0][0] == faces[i][0][1] for i in range(4))

    def _is_solved(self):
        """Check if the entire cube is solved."""
        return all(self._is_face_uniform(face) for face in self.cube.getFaces())

    def _is_face_uniform(self, face):
        """Check if all stickers on a face are the same color."""
        return all(sticker == face[0][0] for row in face for sticker in row)

    def getMoves(self, decorated=True):
        """Get the solution moves."""
        if not self.moves:
            return "Already solved!" if self._is_solved() else "Could not solve."
        
        solution = " ".join(self.moves)
        
        # Simple move optimizer
        solution = solution.replace("U U U U", "").replace("R R R R", "").replace("F F F F", "")
        solution = solution.replace("U U U", "U'").replace("R R R", "R'").replace("F F F", "F'")
        solution = solution.replace("U' U'", "U2").replace("R' R'", "R2").replace("F' F'", "F2")
        solution = solution.replace("U U", "U2").replace("R R", "R2").replace("F F", "F2")
        
        if decorated:
            return f"2x2 Solution: {solution}"
        return solution
