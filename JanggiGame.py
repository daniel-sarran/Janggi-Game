# Author:       Daniel Sarran
# Date:         TODO
# Description:  Korean chess game.

"""
──────────────────────────────────────────────────────────┐
DETAILED TEST DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS │
┌─────────────────────────────────────────────────────────┘
└─ 1. INITIALIZING THE BOARD
        JanggiGame class initializes a _board data member. The _board data member is a Board object.

        The Board object has a data member _squares, which is a list of 90 (9 x 10) Square objects, that hold a piece.
        Each square is represented by its file and row (e.g. 'a1' where 'a' is the file and '1' is the row).

        The game board is populated by a Pieces object, which stores location for each piece on the board. Pieces is
        initialized with default locations for each piece.

        Pieces class has a method "set_board" that places all initial piece locations in the appropriate Squares.

┌─────────────────────────────────────────────────────────
└─ 2. DETERMINING HOW TO REPRESENT PIECES AT A GIVEN LOCATION ON THE BOARD
        Within the Pieces class, there is a dictionary of all players' pieces (keys: players e.g. RED/BLUE, and values:
        a nested dictionary. The nested dictionary key: name of the piece, and the values: Squares occupied by that
        piece.

        Example:    Pieces = {
                        'RED': {
                            'soldier': ['a1', 'b1']
                        }
                    }

┌─────────────────────────────────────────────────────────
└─ 3. DETERMINING HOW TO VALIDATE A GIVEN MOVE ACCORDING TO THE RULES OF EACH PIECE
        Each piece is an object. Each piece class has a function called "get_possible_moves" that returns a set of
        Squares that are, well, possible.

        The JanggiGame "make_move" method then compares to see if the square being moved to is in that list (and also
        checks for out of bounds, & obstructions).

┌─────────────────────────────────────────────────────────
└─ 4. MODIFYING THE BOARD STATE AFTER EACH MOVE
        At the end of JanggiGame "make_move" method, the relevant Squares on the board are updated. If a piece
        is taken, the previous piece is removed, the new piece is set on that square, and the new piece's previous
        Square is cleared.

┌─────────────────────────────────────────────────────────
└─ 5. DETERMINING HOW TO TRACK WHICH PLAYER'S TURN IT IS TO PLAY RIGHT NOW
        JanggiGame has a data member "_side" that holds a 0 for BLUE and a 1 for RED. At the end of "make_move" the side
        is changed to the other player. The colors RED and BLUE are classed as constants which equal 0 or 1 respectively
        to assist with this convention (using the Enum module).

┌─────────────────────────────────────────────────────────
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

┌─────────────────────────────────────────────────────────
└─ 7. DETERMINING WHICH PLAYER HAS WON AND ALSO FIGURING OUT WHEN TO CHECK THAT
        If "is_checkmate" is true, at the end of "make_move" the player making the final move has won. This is checked
        at the beginning of "make move".
"""


class JanggiGame:
    """TODO"""

    def __init__(self):
        """TODO"""
        pass

    def get_game_state(self):
        """Returns a string of the current game state.
        Possible values are the strings "UNFINISHED", "RED_WON", or "BLUE_WON".
        """
        pass

    def set_game_state(self, state):
        """Takes in a string of current game state, updates game state to that state.
        Input is validated such that game state is either 1) unfinished 2) red has won 3) blue has won."""
        pass

    def make_move(self, from_square, to_square):
        """Takes two string parameters of the square moved from and the square moved to.
        If the move is valid, updates game and piece board. Also, a move to-and-from the same square is processed as a
        "pass" for that player."""
        # Invalid moves

        # Square being moved does not contain a piece belonging to current active player
        # return False

        # TODO: check for is_valid() and generate_moves_from_square()
        # The indicated move is not 'legal'
        #   out of bounds
        #   wrong destination for piece
        #   move would put active player in check

        # return False

        # The game has already been won

        # Valid moves

        # TODO: pass - same to and from square

        # Make the move indicated
        # TODO: get piece at location (from_square),
        #       remove piece (from_square),
        #       set piece (to_square, piece)
        #   get piece being moved
        #   remove piece from previous square
        #   set piece at new square

        # TODO: update _attacking
        #   update attacked squares

        # TODO: check for in check,
        #   general's square is in _attacking
        #   check if inactive player is in check

        # TODO: check for checkmate
        #   check if inactive player is in checkmate

    def is_in_check(self, player):
        """Takes a string representing the player. References whether the player's General's square is in the
        '_attacked' list of squares. If so, returns True. Otherwise, returns False."""
        pass

    def is_checkmate(self, player):
        """Takes a player"""
        pass

    def _is_valid_movement(self, from_square, to_square):
        """Takes source and destination squares of an entered movement, returns Boolean value as to whether the move is
        valid or not."""
        pass

    def _end_turn(self):
        """Ends current player's turn."""
        pass

    def get_turn(self):
        """Returns the player whose turn it is to make a move."""
        pass


class Board:
    """Class representing board comprised of 9x10 squares, where each square is specified using "algebraic notation".
    There are 9 files (columns) labeled a-i, and 10 rows labeled 1-10.
    The red side starts on row 1, and the blue side starts on row 10.
    """

    def __init__(self):
        """TODO"""
        pass

    def __str__(self):
        """TODO"""
        pass

    def _initial_squares_setup(self):
        """Initializes board square objects"""
        pass

    def _initial_piece_setup(self):
        """TODO"""
        pass

    def is_attacked(self, square):
        """Takes a square parameters, and determines whether it is currently threatened by an opponent's piece. If the
        square is threatened, returns the square of the opponent's attacking piece. Otherwise returns False."""
        pass

    def update_attacked_squares(self, from_square, to_square):
        """Takes source and destination square of a piece movement. References the piece's 'move_map' to determine all
        squares threatened by piece type based on new location."""
        pass


class Square:
    """A class representing a single Square on the game board. Each square has information about its row and file, and
    the piece on top of the square, if there is one."""

    def __init__(self, file, row, piece_obj=None):
        """TODO"""
        pass

    def get_piece(self):
        """Takes a string of a square, e.g. 'a1', and returns the piece object on that square, otherwise None."""
        pass

    def set_piece(self, piece_obj=None):
        """Takes a square and a piece object, and "places" the piece on the square. When called without a piece
        parameter, clears the square."""
        pass


class Piece:
    """Base class for all game pieces. Stores the owning player as 'BLUE' or 'RED'."""

    def __init__(self, player):
        """TODO"""
        pass

    def get_player(self):
        """Returns the owning player of this piece."""
        pass


class General(Piece):
    """A class representing the General."""

    def __init__(self, player):
        """TODO"""
        super().__init__(player)
        pass

    def move_map(self):
        """Returns a list of 'relative' coordinate-tuples that describe the movement of a General (assuming the current
        square is (0, 0) coordinate location. For example, a piece that can only move "up" by 1 square would return the
        list [(0, 1)]."""
        pass


class Guard(Piece):
    """A class representing a Guard."""

    def __init__(self, player):
        """TODO"""
        super().__init__(player)
        pass

    def move_map(self):
        """Returns a list of 'relative' coordinate-tuples that describe the movement of a Guard (assuming the current
        square is (0, 0) coordinate location. For example, a piece that can only move "up" by 1 square would return the
        list [(0, 1)]."""
        pass


class Horse(Piece):
    """A class representing a Horse."""

    def __init__(self, player):
        """TODO"""
        super().__init__(player)
        pass

    def move_map(self):
        """Returns a list of 'relative' coordinate-tuples that describe the movement of a Horse (assuming the current
        square is (0, 0) coordinate location. For example, a piece that can only move "up" by 1 square would return the
        list [(0, 1)]."""
        pass


class Elephant(Piece):
    """A class representing an elephant."""

    def __init__(self, player):
        """TODO"""
        super().__init__(player)

    def move_map(self):
        """Returns a list of 'relative' coordinate-tuples to describe the movement of an Elephant (assuming the current
        square is (0, 0) coordinate location. For example, a piece that can only move "up" by 1 square would return the
        list [(0, 1)]."""
        pass

    pass


class Chariot(Piece):
    """A class representing a Chariot."""

    def __init(self, player):
        """TODO"""
        super().__init__(player)

    def move_map(self):
        """Returns a list of 'relative' coordinate-tuples that describe the movement of a Chariot (assuming the current
        square is (0, 0) coordinate location. For example, a piece that can only move "up" by 1 square would return the
        list [(0, 1)]."""
        pass


class Cannon(Piece):
    """A class representing a Cannon."""

    def __init__(self, player):
        """TODO"""
        super().__init__(player)
        pass

    def move_map(self):
        """Returns a list of 'relative' coordinate-tuples that describe the movement of a Cannon (assuming the current
        square is (0, 0) coordinate location. For example, a piece that can only move "up" by 1 square would return the
        list [(0, 1)]."""
        pass


class Soldier(Piece):
    """A class representing a Soldier."""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass

    def move_map(self):
        """Returns a list of 'relative' coordinate-tuples that describe the movement of a Soldier (assuming the current
        square is (0, 0) coordinate location. For example, a piece that can only move "up" by 1 square would return the
        list [(0, 1)]. Since Soldiers can only move towards the opposing side, RED move maps are inverted for the row-
        adjustments (e.g. (0, 1) becomes (0, -1)."""
        pass


if __name__ == '__main__':
    game = JanggiGame()
    print(game._board)
    print(game.get_turn())
    game.end_turn()
    print(game.get_turn())
