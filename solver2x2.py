from cube2x2 import Cube2x2
from helper import rawCondense
import copy

class Solver2x2():
    """
    A 2x2 Solver object that uses a simplified CFOP method (Ortega method variant).
    
    For 2x2 cubes, we use:
    1. Face orientation (OLL equivalent) - make one face a solid color
    2. Permutation (PLL equivalent) - arrange the remaining pieces correctly

    Parameters
    ----------
    cube : Cube2x2 object
        The 2x2 cube to be solved.

    Attributes
    ----------
    cube : Cube2x2 object
        The internal copy of the Cube2x2 object.
    """
    
    def __init__(self, cube):
        self.cube = Cube2x2(faces = cube.getFaces())
        self.__faces = self.cube.cube
        self.__forms = []

    def solveCube(self, debug = False, optimize = False):
        """
        Solves the 2x2 cube using Ortega method (simplified CFOP).

        Parameters
        ----------
        debug : bool, default=False
            If set to True, it will print the cube before and after solve.
        optimize : bool, default=False
            If set to True, it will optimize moves.
        """
        self.optimize = optimize
        if(debug):
            print("Before:")
            print(self.cube)
        try:
            self.__forms.append("--align--")
            self.__alignFaces()
            self.__forms.append("--face--")
            self.__solveFace()
            self.__forms.append("--orient--")
            self.__orientLastLayer()
            self.__forms.append("--permute--")
            self.__permuteLastLayer()
        except Exception as exception:
            print(exception.__class__.__name__ + " raised in the program")
        self.__checkComplete()
        if(debug):
            print("After:")
            print(self.cube)
    
    def getMoves(self, decorated = False):
        """
        Returns the moves taken to solve the cube.

        Parameters
        ----------
        decorated : bool, default=False
            If set to True, returns detailed step-by-step moves.

        Returns
        -------
        moves : string
            Moves taken to solve the cube.
        """
        if(decorated):
            current = -1
            alignmentMoves = ""
            faceMoves = ""
            orientMoves = ""
            permuteMoves = ""
            for form in self.__forms:
                if(form == "--align--"):
                    current = 0
                elif(form == "--face--"):
                    current = 1
                elif(form == "--orient--"):
                    current = 2
                elif(form == "--permute--"):
                    current = 3
                else:
                    if(current == 0):
                        alignmentMoves += form
                    elif(current == 1):
                        faceMoves += form
                    elif(current == 2):
                        orientMoves += form
                    elif(current == 3):
                        permuteMoves += form
            moves = ""
            if(bool(alignmentMoves)):
                moves += "For Alignment: " + rawCondense(alignmentMoves) + "\n"
            if(bool(faceMoves)):
                moves += "For First Face: " + rawCondense(faceMoves) + "\n"
            if(bool(orientMoves)):
                moves += "For Orientation: " + rawCondense(orientMoves) + "\n"
            if(bool(permuteMoves)):
                moves += "For Permutation: " + rawCondense(permuteMoves) + "\n"
            moves = moves.strip()
            return moves
        else:
            moves = ""
            for form in self.__forms:
                if(form not in ["--align--", "--face--", "--orient--", "--permute--"]):
                    moves += form + "\n"
            moves = moves.strip()
            return moves
    
    def isSolved(self):
        """
        Checks if the 2x2 cube is solved.

        Returns
        -------
        is_solved : bool
            True if solved, False otherwise.
        """
        is_solved = True
        for i in range(6):
            tar = self.__faces[i][0][0]
            for row in range(2):
                for col in range(2):
                    if(tar != self.__faces[i][row][col]):
                        is_solved = False
        return is_solved
    
    def __checkComplete(self):
        """Check if the cube is completely solved"""
        isDone = True
        for i in range(6):
            tar = self.__faces[i][0][0]
            for row in range(2):
                for col in range(2):
                    if(tar != self.__faces[i][row][col]):
                        isDone = False
        if(not isDone):
            print("<<<ERROR>>>")
            print("The program was not able to solve the 2x2 cube")

    def __move(self, form):
        """Apply moves to the cube and store them"""
        if(bool(form)):
            self.cube.doMoves(form)
            self.__forms.append(form)

    def __alignFaces(self):
        """Align the cube so white is on bottom and green is in front"""
        # Find white face and orient it to bottom
        white_face = -1
        for i in range(6):
            if self.__faces[i][0][0] == "W":
                white_face = i
                break
        
        if white_face == 0:  # Front
            self.__move("x")
        elif white_face == 1:  # Right
            self.__move("z")
        elif white_face == 2:  # Back
            self.__move("x'")
        elif white_face == 3:  # Left
            self.__move("z'")
        elif white_face == 5:  # Top
            self.__move("x2")
        # If white_face == 4, it's already on bottom

        # Now orient green to front
        green_face = -1
        for i in range(4):  # Check side faces only
            if self.__faces[i][0][0] == "G":
                green_face = i
                break
        
        if green_face == 1:  # Right
            self.__move("y'")
        elif green_face == 2:  # Back
            self.__move("y2")
        elif green_face == 3:  # Left
            self.__move("y")

    def __solveFace(self):
        """Solve the white face (bottom) using basic algorithms"""
        # Check if white face is already solved
        white_solved = True
        for row in range(2):
            for col in range(2):
                if self.__faces[4][row][col] != "W":
                    white_solved = False
                    break
        
        if white_solved:
            return
        
        # Simple approach: use basic algorithms to solve white face
        attempts = 0
        while not self.__isWhiteFaceSolved() and attempts < 20:
            # Try different algorithms to get white pieces to bottom
            if self.__faces[5][0][0] == "W":
                self.__move("F D F'")
            elif self.__faces[5][0][1] == "W":
                self.__move("R D R'")
            elif self.__faces[5][1][0] == "W":
                self.__move("L D L'")
            elif self.__faces[5][1][1] == "W":
                self.__move("B D B'")
            else:
                # If no white on top, rotate top layer
                self.__move("U")
            attempts += 1

    def __isWhiteFaceSolved(self):
        """Check if white face is completely solved"""
        for row in range(2):
            for col in range(2):
                if self.__faces[4][row][col] != "W":
                    return False
        return True

    def __orientLastLayer(self):
        """Orient the last layer (make top face one color)"""
        # Check current orientation pattern
        top_colors = []
        for row in range(2):
            for col in range(2):
                top_colors.append(self.__faces[5][row][col])
        
        # Count how many pieces match the center color
        center_color = self.__faces[5][0][0]  # Use first piece as reference
        matching = sum(1 for color in top_colors if color == center_color)
        
        if matching == 4:
            return  # Already oriented
        
        # Apply OLL algorithms for 2x2
        if matching == 0:
            # No pieces match - use algorithm
            self.__move("R U R' U R U2 R'")
        elif matching == 1:
            # One piece matches - try different orientations
            for _ in range(4):
                if self.__faces[5][0][0] == center_color:
                    self.__move("R U R' U R U2 R'")
                    break
                self.__move("U")
        elif matching == 2:
            # Two pieces match - find pattern and apply algorithm
            if (self.__faces[5][0][0] == self.__faces[5][0][1] == center_color) or \
               (self.__faces[5][1][0] == self.__faces[5][1][1] == center_color):
                # Adjacent pieces
                for _ in range(4):
                    if self.__faces[5][0][0] == self.__faces[5][0][1] == center_color:
                        self.__move("R U2 R' U' R U' R'")
                        break
                    self.__move("U")
            else:
                # Diagonal pieces
                self.__move("F R U' R' U' R U R' F'")

    def __permuteLastLayer(self):
        """Permute the last layer to complete the solve"""
        attempts = 0
        while not self.isSolved() and attempts < 10:
            # Check if any face is already complete
            complete_faces = 0
            for face in range(4):  # Check side faces
                if (self.__faces[face][0][0] == self.__faces[face][0][1] == 
                    self.__faces[face][1][0] == self.__faces[face][1][1]):
                    complete_faces += 1
            
            if complete_faces >= 2:
                # Two or more faces complete - use specific algorithm
                self.__move("R U R' F' R U R' U' R' F R2 U' R'")
            elif complete_faces == 1:
                # One face complete - orient and apply algorithm
                for _ in range(4):
                    if (self.__faces[0][0][0] == self.__faces[0][0][1] == 
                        self.__faces[0][1][0] == self.__faces[0][1][1]):
                        self.__move("R U R' F' R U R' U' R' F R2 U' R'")
                        break
                    self.__move("U")
            else:
                # No complete faces - apply corner swap
                self.__move("R U' R F R F' R U R' U' R'")
            
            attempts += 1
            
        # Final adjustment if needed
        for _ in range(4):
            if self.isSolved():
                break
            self.__move("U")
