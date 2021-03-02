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
        self._game_state = 'UNFINISHED'
        self._turn = 'BLUE'
        self._board = Board()

    def get_game_state(self):
        """Returns a string of the current game state.
        Possible values are the strings "UNFINISHED", "RED_WON", or "BLUE_WON".
        """
        return self._game_state

    def set_game_state(self, state):
        """Takes in a string of current game state, updates game state to that state.
        Input is validated such that game state is either 1) unfinished 2) red has won 3) blue has won."""
        if state not in {'UNFINISHED', 'BLUE_WON', 'RED_WON'}:
            return False
        self._game_state = state

    def is_in_check(self, player):
        """TODO"""
        # Returns true if player is in check, returns false otherwise
        pass

    def is_checkmate(self, player):
        """TODO"""
        # 1. can move out of check?
        # 2. can block check?
        # 3. can take the attacker?
        # The king has only 8 spots to move, check if each of those is in _attacked
        # Should have list of squares that are movable, check if one of those blocks every attacker
        # Check who is attacking the king by checking each enemy piece's attacked squares for the king's square
        #   if there's only one attacker, and the attacker's square is in one of your piece's attacked squares, all set!
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
        if self._game_state != 'UNFINISHED':
            return False

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

        self._end_turn()

    def _end_turn(self):
        if self._turn == 'BLUE':
            self._turn = 'RED'

        elif self._turn == 'RED':
            self._turn = 'BLUE'

    def get_turn(self):
        """Returns the player whose turn it is to make a move."""
        return self._turn


class Board:
    """Class representing board comprised of 9x10 squares, where each square is specified using "algebraic notation".
    There are 9 files (columns) labeled a-i, and 10 rows labeled 1-10.
    The red side starts on row 1, and the blue side starts on row 10.
    """

    def __init__(self):
        """TODO"""
        self._files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        self._rows = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self._squares = list()
        self._set_squares()
        self._attacks_by = {'RED': [], 'BLUE': []}

    def __str__(self):
        rows = ''
        for i in range(0, 80, 9):
            rows += ' '.join(map(str, self._squares[i: i + 9]))
            rows += '\n'
        return rows

    def _set_squares(self):
        """Initializes board square objects"""
        for row in self._rows:
            for file in self._files:
                self._squares.extend([Square(file, row)])

    def _set_pieces(self):
        """TODO"""
        pass

    def is_attacked(self, square):
        """TODO"""
        return square in self._attacks_by


class Square:
    """TODO"""

    def __init__(self, file, row, piece_obj=None):
        """TODO"""
        self._file = file
        self._row = row
        self._piece = piece_obj
        self._attacks = []  # attacks is a list of the squares tha

    def __str__(self):
        if self._piece:
            return f'{self._piece}'
        else:
            return f'.'

    def __repr__(self):
        return f'{self._file}{self._row}'


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

    def moves(self, square):
        """TODO"""
        pass


class Guard(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass

    def moves(self, square):
        """TODO"""
        pass


class Horse(Piece):
    """TODO"""

    def __init__(self):
        """TODO"""
        super().__init__()
        pass

    def moves(self, square):
        """TODO"""
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


if __name__ == '__main__':
    game = JanggiGame()
    print(game._board)
    print(game.get_turn())
    game.end_turn()
    print(game.get_turn())
