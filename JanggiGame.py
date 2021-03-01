# Author:       Daniel Sarran
# Date:         TODO
# Description:  Korean chess game.

"""
─────────────────────────────────────────────────────────
DETAILED TEST DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
─────────────────────────────────────────────────────────
└─ 1. INITIALIZING THE BOARD
        There is a Board class that initializes the game board. The game board is made of Square objects and a Pieces
        object. Squares are a class where each square is represented by a string of the file (column) and row for that
        square (e.g. 'a1'), and each Square carries a payload of 'the piece on that square'. Pieces is an object that
        tracks all the pieces locations, which have default placements according to the initial board placement.


└─ 2. DETERMINING HOW TO REPRESENT PIECES AT A GIVEN LOCATION ON THE BOARD
        Within the Pieces class, there is a dictionary of all players' pieces (keys: players e.g. RED/BLUE, and values:
        a nested dictionary. The nested dictionary key: name of the piece, and the values: Squares occupied by that
        piece.

        Example:    Pieces = {
                        'RED': {
                            'soldier': ['a1', 'b1']
                        }
                    }

└─ 3. DETERMINING HOW TO VALIDATE A GIVEN MOVE ACCORDING TO THE RULES OF EACH PIECE
        Each piece is an object. Each piece class has a function called "get_possible_moves" that returns a set of
        Squares that are, well, possible.

        The JanggiGame "make_move" method then compares to see if the square being moved to is in that list (and also
        checks for out of bounds, & obstructions).

└─ 4. MODIFYING THE BOARD STATE AFTER EACH MOVE
        At the end of JanggiGame "make_move" method, the relevant Squares on the board are updated. If a piece
        is taken, the previous piece is removed, the new piece is set on that square, and the new piece's previous
        Square is cleared.

└─ 5. DETERMINING HOW TO TRACK WHICH PLAYER'S TURN IT IS TO PLAY RIGHT NOW
        JanggiGame has a data member "_side" that holds a 0 for BLUE and a 1 for RED. At the end of "make_move" the side
        is changed to the other player. The colors RED and BLUE are classed as constants which equal 0 or 1 respectively
        to assist with this convention (using the Enum module).

└─ 6. DETERMINING HOW TO DETECT THE CHECKMATE SCENARIO
        There is a data member called "_attacking" in Board class. This holds a list of all possible attacked squares,
        and is updated after each move. There is a method called "is_attacked" that searches for a piece's Square within
        "_attacking".

        With that in mind, there is a method in Board called "is_in_check" that determines if a general's Square is in
        the "_attacking" list. If so, there are three conditions for a checkmate:
        1) Can the general move out of check?
        2) Can the check be blocked (or rather, can all checks be blocked)?
        3) Can the player with the checked-general take the attacker?

        Checkmate is determined at the end of make_move(), during the turn of the attacking player (putting the
        defending player in check).

└─ 7. DETERMINING WHICH PLAYER HAS WON AND ALSO FIGURING OUT WHEN TO CHECK THAT
        If "is_checkmate" is true, at the end of "make_move" the player making the final move has won. This is checked
        at the beginning of "make move".
"""

class JanggiGame:
    """TODO"""

    def __init__(self):
        """TODO"""
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """Returns a string of the current game state.
        Possible values are the strings "UNFINISHED", "RED_WON", or "BLUE_WON".
        """
        return self._game_state

    def make_move(self, from_square, to_square):
        """Takes two string parameters of the square moved from and the square moved to.
        If the move is valid, updates game and piece board. Also, a move to-and-from the same square is processed as a
        "pass" for that player."""
        # TODO: 1. check game state

        # TODO: pass - same to and from square

        # TODO: check for is_valid() and generate_moves_from_square()

        # TODO: check for in check,
        #       general's square is in _attacking

        # TODO: check for checkmate

        # TODO: get piece at location (from_square),
        #       remove piece (from_square),
        #       set piece (to_square, piece)

        # TODO: update _attacking

        #


class Board:
    """Class representing board comprised of 9x10 squares, where each square is specified using "algebraic notation".
    There are 9 files (columns) labeled a-i, and 10 rows labeled 1-10.
    The red side starts on row 1, and the blue side starts on row 10.
    """

    def __init__(self):
        """TODO"""
        self._squares = set()  # TODO: list all squares
        self._files = set()
        self._rows = set()
        self._attacking = []

    def is_attacking(self, square):
        """TODO"""
        pass

    def is_in_check(self, square):
        """TODO"""
        pass

    def is_checkmate(self, square):
        """TODO"""
        pass


class Pieces:
    """Class representing all piece locations on the board, as well as the addition and removal of pieces."""

    def __init__(self):
        """TODO"""
        self._blue = dict()
        self._red = dict()
        self._all = set()

    def set_piece_at(self, square, piece):
        """Takes a square and a piece. Updates the piece on that square."""
        # TODO: update piece location (but don't delete the old one)
        pass

    def remove_piece_at(self, square, piece):
        """Takes a square and a piece. Removes the piece from that square."""
        # TODO: remove piece
        pass

    def get_all_piece_locations(self):
        """TODO"""
        return self._all

    def blue_piece_locations(self):
        """Returns locations of all blue pieces."""
        return self._blue

    def red_piece_locations(self):
        """Returns locations of all red pieces."""

    def find_piece_at_square(self, square):
        """Takes a string representing a single board square, returns the piece object on that square."""
        # TODO
        pass

    def reset(self):
        """Resets all pieces to their starting locations on game board."""
        # TODO
        pass

    def clear(self):
        """Clears all pieces from game board."""
        # TODO
        pass


class Square:
    """TODO"""

    def __init__(self):
        """TODO"""


class Player:
    """TODO"""

    def __init__(self):
        """TODO"""
        pass


class Piece:
    """TODO"""

    def __init__(self):
        """TODO"""
        pass


class General(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass


class Guard(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass


class Horse(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass


class Elephant(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass


class Chariot(Piece):
    """TODO"""

    def __init(self):
        """TODO"""
        super().__init__()


class Cannon(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass


class Soldier(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass
