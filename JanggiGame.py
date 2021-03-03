# Author:       Daniel Sarran
# Date:         TODO
# Description:  Korean chess game.

"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                DETAILED TEST DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─ 1. INITIALIZING THE BOARD ──────────────────────────────────────────────────────────────────────────────────────────┘

        JANGGIGAME responsibilities
        - 'JanggiGame' class has a 'Board' object which has 90 'Square' objects representing a 9 x 10 board
        - The 'Board' and 'Squares' are initialized upon construction of JanggiGame
        - Game pieces are tracked via a 'PieceMap' object
        - 'JanggiGame', 'Board', 'Square', and 'PieceMap' interact to handle all player movements across the board.

        BOARD responsibilities
        - The 'Board' is responsible for events and data involving the board as a whole
        - 'Board' interacts with 'Square' and 'Pieces' to handle piece movement, move generation, piece removal, etc.
        - 'Squares' and 'Pieces' are initialized with methods each to get the board setup and place pieces in starting
            positions ('setup_squares' and 'setup_pieces')

        SQUARE responsibilities
        - The 'Square' is responsible for events and data involving one square alone
        - Each 'Square' holds its row and column/file, pointers to surrounding squares, and the 'Piece' on that square

        PIECEMAP responsibilities
        - The 'PieceMap' is responsible for tracking each player's game pieces and their respective locations
        - Initial construction of 'PieceMap' defaults to game piece count and location according to starting positions

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─ 2. DETERMINING HOW TO REPRESENT PIECES AT A GIVEN LOCATION ON THE BOARD ────────────────────────────────────────────┘

        - Game pieces are stored in two places: 'Square' and 'PieceMap'
        - 'Square' primary duty is to track the existence on that square alone
        - 'Pieces' primary duty is to track the entire piece collection on the game board

        SQUARE responsibilities
        - The 'Square' holds a 'Piece' object (representing one individual piece), representing the piece on that square

        PIECEMAP responsibilities
        - The 'Pieces' holds a hash table of BLUE and RED pieces, and their locations
        >>> _pieces = {
                        'BLUE':
                            {   'General': ['e9'],        <-- General location is on 'e9' square
                                'Chariot': ['a10', 'i10'] <-- there are two chariots
                                'Soldier': []             <-- there are no soldiers
                                ...
                            }
                        'RED':
                            {
                               ...
                            }
                        }

        PIECE responsibilities
        - Each individual 'Piece' has its own class and is responsible for calculating its movement and special rules

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─ 3. DETERMINING HOW TO VALIDATE A GIVEN MOVE ACCORDING TO THE RULES OF EACH PIECE ───────────────────────────────────┘

        - The source square (or 'from' square) is checked in 'PieceMap' to determine if it is one of the active player's
            pieces

        I. DETERMINING MOVEMENT FOR EACH PIECE

        PIECE responsibilities
        - Each piece has its own class, that is derived from a base 'Piece' class
        - e.g. Both 'General' 'Chariot' are derived from 'Piece'
        - Each piece class defines the movement available for that particular piece
        - 'Piece' method 'move_map' provides a list of successive moves that would entail a single move, for all
            possible moves around a particular coordinate

        - e.g. 'Horse' may move up one square orthogonal, and one square diagonal:
        - calling 'move_map' will return a list
            >>> [ ['up', 'up-left'], ['up', 'up-right'], ['left', 'up-left']... ]
            representing sequential steps for each possible move to be made

        II. VALIDATING MOVEMENT across player turn, board size, obstructing pieces, etc.

        JANGGIGAME responsibilities
        - 'make_move' calls the 'JanggiGame' method 'valid_player'
        - 'valid_player' passes the current player and the source/from square 'Pieces' to check if the current player
            has a piece at that source square

        PIECE responsibilities
        - The source square ('from' square) is checked against 'Pieces' locations for the active player
        - Does the active player have a piece at the square we are trying to move?

        BOARD responsibilities
        - A 'Board' method 'legal_moves' all the moves from a given piece and location as follows:
                - Iterate through squares and determine...
                - ...out of bounds (e.g. a movement must traverse left, but the 'Square' 'left' pointer is None)
                - ...obstruction by other pieces (e.g. movement instruction is not completed, and there is a piece in
                    one of the traversing squares) - this might also happen through PieceMap I'm not sure yet
                - ...if moving said piece would put general in check
                - ...and a pass is also a legal move (source and destination square are the same)

        IN CHECK SCENARIO
        - 'Board' has an 'attacked' collection which holds all the squares that could be attacked by the enemy
        - 'Attacked' is updated after every player move using the moved 'Piece' 'move_map' method
        - If the active or inactive player's Generals' 'Squares' are in the 'attacked' collection, the 'General' is in
            check - this would be determined by a simple 'is_attacked' method that takes in a Square
        - If a player movement would cause their own General to be in check, the movement is invalid

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─ 4. MODIFYING THE BOARD STATE AFTER EACH MOVE ───────────────────────────────────────────────────────────────────────┘

        JANGGIGAME responsibilities
        - 'JanggiGame' method 'make_move' calls a 'Board' method 'record_move'
        - 'make_move' will calls 'Pieces' method 'update_piece_location'

        BOARD responsibilities
        - 'record_move' calls the 'clear' method for the source square (the 'from' square)
        - 'record_move' calls the 'set' method for the destination square (the 'to' square)

        SQUARE responsibilities
        - 'clear' method removes any piece attribute from that square
        - 'set' method sets a 'piece object' to place on that square

        PIECEMAP responsibilities
        - 'update_piece' removes the old square coordinate, and add the new square coordinate for a given piece
        - Taken pieces simply have their coordinate removed in 'PieceMap', and their location on 'Square' is replaced by
            the new piece

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─ 5. DETERMINING HOW TO TRACK WHICH PLAYER'S TURN IT IS TO PLAY RIGHT NOW ────────────────────────────────────────────┘

        JANGGIGAME responsibilities
        - 'JanggiGame' has a data member 'turn' that holds the name of the player 'BLUE' or 'RED' whose turn it is
        - 'make_move' calls 'valid_player' mentioned above to determine the piece being moved is controlled by the
            proper player
        - 'make_move' uses a helper method 'end_turn' that changes the active turn to the other player

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─ 6. DETERMINING HOW TO DETECT THE CHECKMATE SCENARIO ────────────────────────────────────────────────────────────────┘

        Checkmate is an elevated set of conditions on top of being in check. So 'is_checkmate" method is called by
        'is_in_check'.

        JANGGIGAME responsibilities
        - 'make_move' calls 'is_in_check'
        - 'is_in_check' calls 'is_checkmate'

        BOARD RESPONSIBILITIES
        - 'Board' has an "_attacking" collection that stores all the squares that could be attacked by opposing player
            pieces, this collection is dynamically updated after every successful move

        - 'Board' calls 'is_attacked' method on General's Square to see if the General is under attack

        - If general is in check, there are three conditions for a checkmate:
            1) Can the general move out of check?
                - 'Board' already has method 'legal_moves' to determine this, if there are no moves then...
            2) Can the check be blocked (or rather, can all checks be blocked)?
                - For the attacking piece, iterate through the move sequence that leads to a check, and store those
                    squares
                - Then check 'legal_moves' for any non-General pieces that can move to those squares
            3) Can the player with the checked-general take the attacker?
                - check if the 'attacked' collection holds the square of the piece putting the general in check

        - Finally, checkmate is determined at the end of 'make_move' method, during the turn of the attacking player
            (the player putting the other general in check, before the in-check player starts their turn)

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
└─ 7. DETERMINING WHICH PLAYER HAS WON AND ALSO FIGURING OUT WHEN TO CHECK THAT ───────────────────────────────────────┘

        JANGGIGAME responsibilities
        - If "is_checkmate" method returns True within 'is_in_check' method (at the end of "make_move"), then the game
            will be updated to the winning player (e.g. 'BLUE_WON')

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
"""


class JanggiGame:
    """
    A class representing the strategy board game sometimes referred to as 'Korean Chess'. Two players control pieces
    on a 9 x 10 board. Each piece moves in a different way in order to protect their 'General'. The objective is to
    put the opponent's General into checkmate!
    """

    def __init__(self):
        """Initializes a JanggiGame object. Sets up starting player, board and pieces."""
        self._board = Board()
        self._turn = 'BLUE'
        self._game_state = 'UNFINISHED'

    def get_game_state(self):
        """
        Returns a string of the current game state.
        Possible values are the strings "UNFINISHED", "RED_WON", or "BLUE_WON".
        """
        return self._game_state

    def set_game_state(self, state):
        """
        Takes in a string of current game state, updates game state to that state.

        :param  state    'UNFINISHED', 'BLUE_WON', 'RED_WON'
        :type   state     string
        """
        pass

    def make_move(self, from_square, to_square):
        """
        Takes two string parameters of the square moved from and the square moved to.
        If the move is valid, updates game and piece board. A move to-and-from the same square is processed as a
        "pass" for that player. Checks for 'check' and 'checkmate', and records movement on game board and pieces.

        :param from_square  The source square the moving piece is coming from
        :type  from_square  Square object
        :param to_square    The source square the moving piece is coming from
        :type  to_square    Square object
        """
        pass

    def is_in_check(self, player):
        """
        Takes a string representing the player. References whether the player's General's square is in the
        '_attacked' list of squares. If so, returns True. Otherwise, returns False.

        :param  player  One of the players 'BLUE' or 'RED'
        :type   player  string
        """
        pass

    def is_checkmate(self, player):
        """
        Takes a string representing a player, returns a True if player is in checkmate, otherwise returns False.

        :param  player  One of the players 'BLUE' or 'RED'
        :type   player  string
        """
        pass

    def _is_valid_movement(self, from_square, to_square):
        """
        Takes source and destination squares of an entered movement, returns Boolean value as to whether the move is
        valid or not. Checks for out of bounds, opposing piece obstructions, and proper piece movement.

        :param from_square  The source square the moving piece is coming from
        :type  from_square  Square object
        :param to_square    The source square the moving piece is coming from
        :type  to_square    Square object
        """
        pass

    def _end_turn(self):
        """Ends current player's turn."""
        pass

    def get_turn(self):
        """Returns the player whose turn it is to make a move."""
        return self._turn


class Board:
    """
    Class representing board comprised of 9x10 squares, where each square is specified using "algebraic notation".
    There are 9 files (columns) labeled a-i, and 10 rows labeled 1-10. The red side starts on row 1, and the blue side
    starts on row 10.
    """

    def __init__(self):
        """Initializes a Board object. A board is made of of 90 Square objects."""
        self._squares = []
        self._pieces = PieceMap()
        self._attacked = []
        self._setup_squares()
        pass

    def __str__(self):
        """String representation of a board."""
        pass

    def _setup_squares(self):
        """Instantiates 90 square objects with row and file."""
        pass

    def is_attacked(self, square):
        """
        Takes a square parameters, and determines whether it is currently under attack by an opponent's piece. If the
        square is under attack, returns the square of the opponent's attacking piece. Otherwise returns False.

        :param  square  A board square
        :type   square  Square object
        """
        pass

    def update_attacked(self, from_square, to_square):
        """
        Takes source and destination square of a piece movement. References the piece's 'move_map' to determine all
        squares threatened by piece type based on new location.

        :param from_square: The source square the moving piece is coming from
        :type  from_square: Square object
        :param to_square:   The destination square the moving piece is coming from
        :type  to_square:   Square object
        """
        pass

    def legal_moves(self, moves_list):
        """
        Validates a list of moves from perspective of the game board. Filters out of bounds moves, obstructed moves,
        and moves that leave the player in check.

        :param  moves_list: A list of lists -- the inner lists are sequential instructions that complete a move
                            e.g. [ ['up', 'up', 'left'] ]
        :type   moves_list: list
        """
        pass

    def record_move(self, from_square, to_square):
        """
        Finalizes movement of a piece from one square to another.

        :param from_square: The source square the moving piece is coming from
        :type  from_square: Square object
        :param  to_square:  The destination square the moving piece is moving to
        :type   to_square:  Square object
        """
        pass


class Square:
    """
    A class representing a single Square on the game board. Each square has information about its row and file, and
    the piece on top of the square, if there is one.
    """

    def __init__(self, file, row):
        """
        Initializes a Square with file/column and row.

        :param  file:   The file or column of the square e.g. 'a', 'b', 'c', ...
        :type   file:   string
        :param  row:    The row of the square e.g. '1', '2', '3', ...
        :type   row:    string
        """
        self._file = file
        self._row = row
        self._piece = None
        self._up = None
        self._up_left = None
        self._left = None
        self._down_left = None
        self._down = None
        self._down_right = None
        self._right = None
        self._up_right = None

    def get_piece_at(self, square):
        """
        Takes square object, e.g. 'a1', and returns the piece object on that square, otherwise returns None.

        :param  square: The square to retrieve the unit from
        :type   square: Square object
        """
        pass

    def clear_piece_at(self, square):
        """
        Clears the square of any pieces.

        :param  square: The square to clear
        :type   square: Square object
        """
        pass

    def set_piece_at(self, square, piece):
        """
        Places a piece in the target square.

        :param  square: The square to set the piece on
        :type   square: Square object
        :param  piece:  The piece to set on the square
        :type   piece:  Piece object (could be any derived class of Piece - e.g. Horse, General, etc.)
        """
        pass


class PieceMap:
    """A class representing the location and interaction of game pieces."""

    def __init__(self):
        """Initializes a PieceMap class with starting positions for all pieces for each player."""
        pass

    def update_piece(self, piece, square_to_add=None, square_to_remove=None):
        """
        Takes a piece object, and updates its location in the PieceMap. Optional parameters to add or remove depending
        on desired action.

        :param  piece:  The piece whose locations are being updated
        :type   piece:  Piece object or child of Piece
        :param  square_to_add:  The new location of a moved piece
        :type   square_to_add:  Square object
        :param  square_to_remove:   The previous location of a moved piece, OR the location of a taken piece
        :type   square_to_remove:   Square object
        """
        pass


class Piece:
    """Base class for all game pieces to be derived from."""

    def __init__(self, player):
        """Initializes the Piece base class. Stores the owning player as 'BLUE' or 'RED'."""
        pass

    def get_player(self):
        """Returns the owning player of this piece."""
        pass


class General(Piece):
    """A class representing the General."""

    def __init__(self, player):
        """Initializes a General and its movement mechanism."""
        super().__init__(player)
        pass

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


class Guard(Piece):
    """A class representing a Guard."""

    def __init__(self, player):
        """Initializes a Guard and its movement mechanism."""
        super().__init__(player)
        pass

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


class Horse(Piece):
    """A class representing a Horse."""

    def __init__(self, player):
        """Initializes a Horse and its movement mechanism."""
        super().__init__(player)
        pass

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


class Elephant(Piece):
    """A class representing an elephant."""

    def __init__(self, player):
        """Initializes an Elephant and its movement mechanism."""
        super().__init__(player)

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


class Chariot(Piece):
    """A class representing a Chariot."""

    def __init(self, player):
        """Initializes a Chariot and its movement mechanism."""
        super().__init__(player)

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


class Cannon(Piece):
    """A class representing a Cannon."""

    def __init__(self, player):
        """Initializes a Cannon and its movement mechanism."""
        super().__init__(player)
        pass

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


class Soldier(Piece):
    """A class representing a Soldier."""

    def __init__(self, player):
        """Initializes a Soldier and its movement mechanism."""
        super().__init__(player)
        pass

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


if __name__ == '__main__':
    game = JanggiGame()
    print(game._board)
    print(game.get_turn())
    game._end_turn()
    print(game.get_turn())
