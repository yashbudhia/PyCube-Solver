from helper import parseFormula
import copy

class Cube2x2:
    """
    An object which models a 2x2 Rubik's cube and can be moved using formulas that follow the standard cube representation.

    Parameters
    ----------
    faces : string, default="None"
        Set the initial state of the cube to a specific cube faces matrix array.

    Attributes
    ----------
    cube : list of size (6, 2, 2)
        The internal cube faces matrix array for the 2x2 cube object.
    
    Example
    -------
    >>> cb = Cube2x2()
    >>> cb.doMoves("RU")
    >>> print(cb)
        YY
        YY
    BR OY GO
    RR GG OO
        WW
        WW
    """
    
    def __init__(self, faces = "None"):
        # Orientation mapping for 2x2 cube (similar to 3x3 but corners only)
        self.orientation = [[5, 1, 4, 3], [5, 2, 4, 0], [5, 3, 4, 1], [5, 0, 4, 2], [0, 1, 2, 3], [2, 1, 0, 3]]
        # Rotation mapping for 2x2 cube (corners only)
        self.rotmap = [[[1, 0], [1, 1], [0, 0], [1, 0], [0, 0], [1, 0], [0, 1], [0, 0], [1, 1], [0, 1]], 
                       [[1, 1], [0, 1], [0, 0], [1, 0], [1, 1], [0, 1], [1, 1], [0, 1], [1, 1], [0, 1]], 
                       [[0, 1], [0, 0], [0, 0], [1, 0], [1, 0], [1, 1], [1, 1], [0, 1], [1, 1], [0, 1]], 
                       [[0, 0], [1, 0], [0, 0], [1, 0], [0, 0], [1, 0], [0, 0], [1, 0], [1, 1], [0, 1]], 
                       [[1, 0], [1, 1], [1, 0], [1, 1], [1, 0], [1, 1], [1, 0], [1, 1]], 
                       [[0, 1], [0, 0], [0, 1], [0, 0], [0, 1], [0, 0], [0, 1], [0, 0]]]
        self.sideTocmap = ["G", "O", "B", "R", "W", "Y"]
        if(faces == "None"):
            self.cube = [[[self.sideTocmap[c]] * 2 for _ in range(2)] for c in range(6)]
        else:
            self.cube = faces

    def __str__(self):
        pstr = ""
        # Top face
        for i in range(2):
            pstr += "  "
            for j in range(2):
                pstr += self.cube[5][i][j]
            pstr += "\n"
        # Middle row (left, front, right, back)
        for i in range(2):
            for face in [3, 0, 1, 2]:
                for j in range(2):
                    pstr += self.cube[face][i][j]
                pstr += " " if face != 2 else ""
            pstr += "\n"
        # Bottom face
        for i in range(2):
            pstr += "  "
            for j in range(2):
                pstr += self.cube[4][i][j]
            pstr += "\n"
        return pstr

    def getFaces(self):
        """
        Returns the state of the cube.

        Returns
        -------
        cube : list of size (6, 2, 2)
            The internal cube faces matrix array for the cube object.
        """
        return copy.deepcopy(self.cube)

    def doMoves(self, formula):
        """
        Apply the given formula to this cube.

        Parameters
        ----------
        formula : string
            Formula to be applied to this cube. Example: "R U' L D2 F'"
        """
        moves = parseFormula(formula)
        for move in moves:
            self.__applyMove(move)

    def __applyMove(self, move):
        """Apply a single move to the cube"""
        moveType = move["move"]
        inverted = move["inverted"]
        turns = move["turn_count"]
        
        for _ in range(turns):
            if moveType == "R":
                self.__rotateRightFace(inverted)
            elif moveType == "L":
                self.__rotateLeftFace(inverted)
            elif moveType == "U":
                self.__rotateUpFace(inverted)
            elif moveType == "D":
                self.__rotateDownFace(inverted)
            elif moveType == "F":
                self.__rotateFrontFace(inverted)
            elif moveType == "B":
                self.__rotateBackFace(inverted)

    def __rotateRightFace(self, inverted):
        """Rotate the right face"""
        self.__rotateFace(1, inverted)
        # Cycle edges for 2x2 cube
        if not inverted:
            temp = [self.cube[5][0][1], self.cube[5][1][1]]
            self.cube[5][0][1], self.cube[5][1][1] = self.cube[0][0][1], self.cube[0][1][1]
            self.cube[0][0][1], self.cube[0][1][1] = self.cube[4][0][1], self.cube[4][1][1]
            self.cube[4][0][1], self.cube[4][1][1] = self.cube[2][1][0], self.cube[2][0][0]
            self.cube[2][1][0], self.cube[2][0][0] = temp[0], temp[1]
        else:
            temp = [self.cube[5][0][1], self.cube[5][1][1]]
            self.cube[5][0][1], self.cube[5][1][1] = self.cube[2][1][0], self.cube[2][0][0]
            self.cube[2][1][0], self.cube[2][0][0] = self.cube[4][0][1], self.cube[4][1][1]
            self.cube[4][0][1], self.cube[4][1][1] = self.cube[0][0][1], self.cube[0][1][1]
            self.cube[0][0][1], self.cube[0][1][1] = temp[0], temp[1]

    def __rotateLeftFace(self, inverted):
        """Rotate the left face"""
        self.__rotateFace(3, inverted)
        if not inverted:
            temp = [self.cube[5][0][0], self.cube[5][1][0]]
            self.cube[5][0][0], self.cube[5][1][0] = self.cube[2][1][1], self.cube[2][0][1]
            self.cube[2][1][1], self.cube[2][0][1] = self.cube[4][0][0], self.cube[4][1][0]
            self.cube[4][0][0], self.cube[4][1][0] = self.cube[0][0][0], self.cube[0][1][0]
            self.cube[0][0][0], self.cube[0][1][0] = temp[0], temp[1]
        else:
            temp = [self.cube[5][0][0], self.cube[5][1][0]]
            self.cube[5][0][0], self.cube[5][1][0] = self.cube[0][0][0], self.cube[0][1][0]
            self.cube[0][0][0], self.cube[0][1][0] = self.cube[4][0][0], self.cube[4][1][0]
            self.cube[4][0][0], self.cube[4][1][0] = self.cube[2][1][1], self.cube[2][0][1]
            self.cube[2][1][1], self.cube[2][0][1] = temp[0], temp[1]

    def __rotateUpFace(self, inverted):
        """Rotate the up face"""
        self.__rotateFace(5, inverted)
        if not inverted:
            temp = [self.cube[0][0][0], self.cube[0][0][1]]
            self.cube[0][0][0], self.cube[0][0][1] = self.cube[3][0][0], self.cube[3][0][1]
            self.cube[3][0][0], self.cube[3][0][1] = self.cube[2][0][0], self.cube[2][0][1]
            self.cube[2][0][0], self.cube[2][0][1] = self.cube[1][0][0], self.cube[1][0][1]
            self.cube[1][0][0], self.cube[1][0][1] = temp[0], temp[1]
        else:
            temp = [self.cube[0][0][0], self.cube[0][0][1]]
            self.cube[0][0][0], self.cube[0][0][1] = self.cube[1][0][0], self.cube[1][0][1]
            self.cube[1][0][0], self.cube[1][0][1] = self.cube[2][0][0], self.cube[2][0][1]
            self.cube[2][0][0], self.cube[2][0][1] = self.cube[3][0][0], self.cube[3][0][1]
            self.cube[3][0][0], self.cube[3][0][1] = temp[0], temp[1]

    def __rotateDownFace(self, inverted):
        """Rotate the down face"""
        self.__rotateFace(4, inverted)
        if not inverted:
            temp = [self.cube[0][1][0], self.cube[0][1][1]]
            self.cube[0][1][0], self.cube[0][1][1] = self.cube[1][1][0], self.cube[1][1][1]
            self.cube[1][1][0], self.cube[1][1][1] = self.cube[2][1][0], self.cube[2][1][1]
            self.cube[2][1][0], self.cube[2][1][1] = self.cube[3][1][0], self.cube[3][1][1]
            self.cube[3][1][0], self.cube[3][1][1] = temp[0], temp[1]
        else:
            temp = [self.cube[0][1][0], self.cube[0][1][1]]
            self.cube[0][1][0], self.cube[0][1][1] = self.cube[3][1][0], self.cube[3][1][1]
            self.cube[3][1][0], self.cube[3][1][1] = self.cube[2][1][0], self.cube[2][1][1]
            self.cube[2][1][0], self.cube[2][1][1] = self.cube[1][1][0], self.cube[1][1][1]
            self.cube[1][1][0], self.cube[1][1][1] = temp[0], temp[1]

    def __rotateFrontFace(self, inverted):
        """Rotate the front face"""
        self.__rotateFace(0, inverted)
        if not inverted:
            temp = [self.cube[5][1][0], self.cube[5][1][1]]
            self.cube[5][1][0], self.cube[5][1][1] = self.cube[3][1][1], self.cube[3][0][1]
            self.cube[3][1][1], self.cube[3][0][1] = self.cube[4][0][1], self.cube[4][0][0]
            self.cube[4][0][1], self.cube[4][0][0] = self.cube[1][0][0], self.cube[1][1][0]
            self.cube[1][0][0], self.cube[1][1][0] = temp[0], temp[1]
        else:
            temp = [self.cube[5][1][0], self.cube[5][1][1]]
            self.cube[5][1][0], self.cube[5][1][1] = self.cube[1][0][0], self.cube[1][1][0]
            self.cube[1][0][0], self.cube[1][1][0] = self.cube[4][0][1], self.cube[4][0][0]
            self.cube[4][0][1], self.cube[4][0][0] = self.cube[3][1][1], self.cube[3][0][1]
            self.cube[3][1][1], self.cube[3][0][1] = temp[0], temp[1]

    def __rotateBackFace(self, inverted):
        """Rotate the back face"""
        self.__rotateFace(2, inverted)
        if not inverted:
            temp = [self.cube[5][0][0], self.cube[5][0][1]]
            self.cube[5][0][0], self.cube[5][0][1] = self.cube[1][0][1], self.cube[1][1][1]
            self.cube[1][0][1], self.cube[1][1][1] = self.cube[4][1][1], self.cube[4][1][0]
            self.cube[4][1][1], self.cube[4][1][0] = self.cube[3][1][0], self.cube[3][0][0]
            self.cube[3][1][0], self.cube[3][0][0] = temp[0], temp[1]
        else:
            temp = [self.cube[5][0][0], self.cube[5][0][1]]
            self.cube[5][0][0], self.cube[5][0][1] = self.cube[3][1][0], self.cube[3][0][0]
            self.cube[3][1][0], self.cube[3][0][0] = self.cube[4][1][1], self.cube[4][1][0]
            self.cube[4][1][1], self.cube[4][1][0] = self.cube[1][0][1], self.cube[1][1][1]
            self.cube[1][0][1], self.cube[1][1][1] = temp[0], temp[1]

    def __rotateFace(self, face, inverted):
        """Rotate a face clockwise or counterclockwise"""
        if not inverted:
            # Clockwise rotation for 2x2
            temp = self.cube[face][0][0]
            self.cube[face][0][0] = self.cube[face][1][0]
            self.cube[face][1][0] = self.cube[face][1][1]
            self.cube[face][1][1] = self.cube[face][0][1]
            self.cube[face][0][1] = temp
        else:
            # Counterclockwise rotation for 2x2
            temp = self.cube[face][0][0]
            self.cube[face][0][0] = self.cube[face][0][1]
            self.cube[face][0][1] = self.cube[face][1][1]
            self.cube[face][1][1] = self.cube[face][1][0]
            self.cube[face][1][0] = temp
