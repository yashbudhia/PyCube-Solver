from helper import parseFormula
import copy

class Cube4x4:
    """
    An object which models a 4x4 Rubik's cube and can be moved using formulas that follow the standard cube representation.

    Parameters
    ----------
    faces : string, default="None"
        Set the initial state of the cube to a specific cube faces matrix array.

    Attributes
    ----------
    cube : list of size (6, 4, 4)
        The internal cube faces matrix array for the 4x4 cube object.
    
    Example
    -------
    >>> cb = Cube4x4()
    >>> cb.doMoves("R U R' U'")
    >>> print(cb)
    """
    
    def __init__(self, faces = "None"):
        self.sideTocmap = ["G", "O", "B", "R", "W", "Y"]
        if(faces == "None"):
            self.cube = [[[self.sideTocmap[c]] * 4 for _ in range(4)] for c in range(6)]
        else:
            self.cube = faces

    def getFacesAsTuple(self):
        """Return the faces as a tuple of tuples for hashing."""
        return tuple(tuple(map(tuple, face)) for face in self.cube)

    def __str__(self):
        pstr = ""
        # Top face
        for i in range(4):
            pstr += "    "
            for j in range(4):
                pstr += self.cube[5][i][j]
            pstr += "\n"
        # Middle row (left, front, right, back)
        for i in range(4):
            for face in [3, 0, 1, 2]:
                for j in range(4):
                    pstr += self.cube[face][i][j]
                pstr += " " if face != 2 else ""
            pstr += "\n"
        # Bottom face
        for i in range(4):
            pstr += "    "
            for j in range(4):
                pstr += self.cube[4][i][j]
            pstr += "\n"
        return pstr

    def getFaces(self):
        """
        Returns the state of the cube.

        Returns
        -------
        cube : list of size (6, 4, 4)
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
        if move == "R":
            self.__rotateRightFace(False)
        elif move == "RP":
            self.__rotateRightFace(True)
        elif move == "L":
            self.__rotateLeftFace(False)
        elif move == "LP":
            self.__rotateLeftFace(True)
        elif move == "U":
            self.__rotateUpFace(False)
        elif move == "UP":
            self.__rotateUpFace(True)
        elif move == "D":
            self.__rotateDownFace(False)
        elif move == "DP":
            self.__rotateDownFace(True)
        elif move == "F":
            self.__rotateFrontFace(False)
        elif move == "FP":
            self.__rotateFrontFace(True)
        elif move == "B":
            self.__rotateBackFace(False)
        elif move == "BP":
            self.__rotateBackFace(True)
        # Wide moves for 4x4
        elif move == "r":
            self.__rotateRightWide(False)
        elif move == "rP":
            self.__rotateRightWide(True)
        elif move == "l":
            self.__rotateLeftWide(False)
        elif move == "lP":
            self.__rotateLeftWide(True)
        elif move == "u":
            self.__rotateUpWide(False)
        elif move == "uP":
            self.__rotateUpWide(True)
        elif move == "d":
            self.__rotateDownWide(False)
        elif move == "dP":
            self.__rotateDownWide(True)
        elif move == "f":
            self.__rotateFrontWide(False)
        elif move == "fP":
            self.__rotateFrontWide(True)
        elif move == "b":
            self.__rotateBackWide(False)
        elif move == "bP":
            self.__rotateBackWide(True)

    def __rotateRightFace(self, inverted):
        """Rotate the right face (only outer layer)"""
        self.__rotateFace(1, inverted)
        # Cycle edges for 4x4 cube (outer layer only)
        if not inverted:
            temp = [self.cube[5][i][3] for i in range(4)]
            for i in range(4):
                self.cube[5][i][3] = self.cube[0][i][3]
                self.cube[0][i][3] = self.cube[4][i][3]
                self.cube[4][i][3] = self.cube[2][3-i][0]
                self.cube[2][3-i][0] = temp[i]
        else:
            temp = [self.cube[5][i][3] for i in range(4)]
            for i in range(4):
                self.cube[5][i][3] = self.cube[2][3-i][0]
                self.cube[2][3-i][0] = self.cube[4][i][3]
                self.cube[4][i][3] = self.cube[0][i][3]
                self.cube[0][i][3] = temp[i]

    def __rotateRightWide(self, inverted):
        """Rotate both right layers (wide move)"""
        self.__rotateRightFace(inverted)
        # Also rotate the inner right layer
        if not inverted:
            temp = [self.cube[5][i][2] for i in range(4)]
            for i in range(4):
                self.cube[5][i][2] = self.cube[0][i][2]
                self.cube[0][i][2] = self.cube[4][i][2]
                self.cube[4][i][2] = self.cube[2][3-i][1]
                self.cube[2][3-i][1] = temp[i]
        else:
            temp = [self.cube[5][i][2] for i in range(4)]
            for i in range(4):
                self.cube[5][i][2] = self.cube[2][3-i][1]
                self.cube[2][3-i][1] = self.cube[4][i][2]
                self.cube[4][i][2] = self.cube[0][i][2]
                self.cube[0][i][2] = temp[i]

    def __rotateLeftFace(self, inverted):
        """Rotate the left face (only outer layer)"""
        self.__rotateFace(3, inverted)
        if not inverted:
            temp = [self.cube[5][i][0] for i in range(4)]
            for i in range(4):
                self.cube[5][i][0] = self.cube[2][3-i][3]
                self.cube[2][3-i][3] = self.cube[4][i][0]
                self.cube[4][i][0] = self.cube[0][i][0]
                self.cube[0][i][0] = temp[i]
        else:
            temp = [self.cube[5][i][0] for i in range(4)]
            for i in range(4):
                self.cube[5][i][0] = self.cube[0][i][0]
                self.cube[0][i][0] = self.cube[4][i][0]
                self.cube[4][i][0] = self.cube[2][3-i][3]
                self.cube[2][3-i][3] = temp[i]

    def __rotateLeftWide(self, inverted):
        """Rotate both left layers (wide move)"""
        self.__rotateLeftFace(inverted)
        # Also rotate the inner left layer
        if not inverted:
            temp = [self.cube[5][i][1] for i in range(4)]
            for i in range(4):
                self.cube[5][i][1] = self.cube[2][3-i][2]
                self.cube[2][3-i][2] = self.cube[4][i][1]
                self.cube[4][i][1] = self.cube[0][i][1]
                self.cube[0][i][1] = temp[i]
        else:
            temp = [self.cube[5][i][1] for i in range(4)]
            for i in range(4):
                self.cube[5][i][1] = self.cube[0][i][1]
                self.cube[0][i][1] = self.cube[4][i][1]
                self.cube[4][i][1] = self.cube[2][3-i][2]
                self.cube[2][3-i][2] = temp[i]

    def __rotateUpFace(self, inverted):
        """Rotate the up face (only outer layer)"""
        self.__rotateFace(5, inverted)
        if not inverted:
            temp = [self.cube[0][0][j] for j in range(4)]
            for j in range(4):
                self.cube[0][0][j] = self.cube[3][0][j]
                self.cube[3][0][j] = self.cube[2][0][j]
                self.cube[2][0][j] = self.cube[1][0][j]
                self.cube[1][0][j] = temp[j]
        else:
            temp = [self.cube[0][0][j] for j in range(4)]
            for j in range(4):
                self.cube[0][0][j] = self.cube[1][0][j]
                self.cube[1][0][j] = self.cube[2][0][j]
                self.cube[2][0][j] = self.cube[3][0][j]
                self.cube[3][0][j] = temp[j]

    def __rotateUpWide(self, inverted):
        """Rotate both up layers (wide move)"""
        self.__rotateUpFace(inverted)
        # Also rotate the inner up layer
        if not inverted:
            temp = [self.cube[0][1][j] for j in range(4)]
            for j in range(4):
                self.cube[0][1][j] = self.cube[3][1][j]
                self.cube[3][1][j] = self.cube[2][1][j]
                self.cube[2][1][j] = self.cube[1][1][j]
                self.cube[1][1][j] = temp[j]
        else:
            temp = [self.cube[0][1][j] for j in range(4)]
            for j in range(4):
                self.cube[0][1][j] = self.cube[1][1][j]
                self.cube[1][1][j] = self.cube[2][1][j]
                self.cube[2][1][j] = self.cube[3][1][j]
                self.cube[3][1][j] = temp[j]

    def __rotateDownFace(self, inverted):
        """Rotate the down face (only outer layer)"""
        self.__rotateFace(4, inverted)
        if not inverted:
            temp = [self.cube[0][3][j] for j in range(4)]
            for j in range(4):
                self.cube[0][3][j] = self.cube[1][3][j]
                self.cube[1][3][j] = self.cube[2][3][j]
                self.cube[2][3][j] = self.cube[3][3][j]
                self.cube[3][3][j] = temp[j]
        else:
            temp = [self.cube[0][3][j] for j in range(4)]
            for j in range(4):
                self.cube[0][3][j] = self.cube[3][3][j]
                self.cube[3][3][j] = self.cube[2][3][j]
                self.cube[2][3][j] = self.cube[1][3][j]
                self.cube[1][3][j] = temp[j]

    def __rotateDownWide(self, inverted):
        """Rotate both down layers (wide move)"""
        self.__rotateDownFace(inverted)
        # Also rotate the inner down layer
        if not inverted:
            temp = [self.cube[0][2][j] for j in range(4)]
            for j in range(4):
                self.cube[0][2][j] = self.cube[1][2][j]
                self.cube[1][2][j] = self.cube[2][2][j]
                self.cube[2][2][j] = self.cube[3][2][j]
                self.cube[3][2][j] = temp[j]
        else:
            temp = [self.cube[0][2][j] for j in range(4)]
            for j in range(4):
                self.cube[0][2][j] = self.cube[3][2][j]
                self.cube[3][2][j] = self.cube[2][2][j]
                self.cube[2][2][j] = self.cube[1][2][j]
                self.cube[1][2][j] = temp[j]

    def __rotateFrontFace(self, inverted):
        """Rotate the front face (only outer layer)"""
        self.__rotateFace(0, inverted)
        if not inverted:
            temp = [self.cube[5][3][j] for j in range(4)]
            for j in range(4):
                self.cube[5][3][j] = self.cube[3][3-j][3]
                self.cube[3][3-j][3] = self.cube[4][0][3-j]
                self.cube[4][0][3-j] = self.cube[1][j][0]
                self.cube[1][j][0] = temp[j]
        else:
            temp = [self.cube[5][3][j] for j in range(4)]
            for j in range(4):
                self.cube[5][3][j] = self.cube[1][j][0]
                self.cube[1][j][0] = self.cube[4][0][3-j]
                self.cube[4][0][3-j] = self.cube[3][3-j][3]
                self.cube[3][3-j][3] = temp[j]

    def __rotateFrontWide(self, inverted):
        """Rotate both front layers (wide move)"""
        self.__rotateFrontFace(inverted)
        # Also rotate the inner front layer
        if not inverted:
            temp = [self.cube[5][2][j] for j in range(4)]
            for j in range(4):
                self.cube[5][2][j] = self.cube[3][3-j][2]
                self.cube[3][3-j][2] = self.cube[4][1][3-j]
                self.cube[4][1][3-j] = self.cube[1][j][1]
                self.cube[1][j][1] = temp[j]
        else:
            temp = [self.cube[5][2][j] for j in range(4)]
            for j in range(4):
                self.cube[5][2][j] = self.cube[1][j][1]
                self.cube[1][j][1] = self.cube[4][1][3-j]
                self.cube[4][1][3-j] = self.cube[3][3-j][2]
                self.cube[3][3-j][2] = temp[j]

    def __rotateBackFace(self, inverted):
        """Rotate the back face (only outer layer)"""
        self.__rotateFace(2, inverted)
        if not inverted:
            temp = [self.cube[5][0][j] for j in range(4)]
            for j in range(4):
                self.cube[5][0][j] = self.cube[1][j][3]
                self.cube[1][j][3] = self.cube[4][3][3-j]
                self.cube[4][3][3-j] = self.cube[3][3-j][0]
                self.cube[3][3-j][0] = temp[j]
        else:
            temp = [self.cube[5][0][j] for j in range(4)]
            for j in range(4):
                self.cube[5][0][j] = self.cube[3][3-j][0]
                self.cube[3][3-j][0] = self.cube[4][3][3-j]
                self.cube[4][3][3-j] = self.cube[1][j][3]
                self.cube[1][j][3] = temp[j]

    def __rotateBackWide(self, inverted):
        """Rotate both back layers (wide move)"""
        self.__rotateBackFace(inverted)
        # Also rotate the inner back layer
        if not inverted:
            temp = [self.cube[5][1][j] for j in range(4)]
            for j in range(4):
                self.cube[5][1][j] = self.cube[1][j][2]
                self.cube[1][j][2] = self.cube[4][2][3-j]
                self.cube[4][2][3-j] = self.cube[3][3-j][1]
                self.cube[3][3-j][1] = temp[j]
        else:
            temp = [self.cube[5][1][j] for j in range(4)]
            for j in range(4):
                self.cube[5][1][j] = self.cube[3][3-j][1]
                self.cube[3][3-j][1] = self.cube[4][2][3-j]
                self.cube[4][2][3-j] = self.cube[1][j][2]
                self.cube[1][j][2] = temp[j]

    def __rotateFace(self, face, inverted):
        """Rotate a face clockwise or counterclockwise"""
        if not inverted:
            # Clockwise rotation for 4x4
            temp = [[self.cube[face][i][j] for j in range(4)] for i in range(4)]
            for i in range(4):
                for j in range(4):
                    self.cube[face][i][j] = temp[3-j][i]
        else:
            # Counterclockwise rotation for 4x4
            temp = [[self.cube[face][i][j] for j in range(4)] for i in range(4)]
            for i in range(4):
                for j in range(4):
                    self.cube[face][i][j] = temp[j][3-i]
