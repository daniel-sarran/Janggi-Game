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
        >> _pieces = {
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
            >> [ ['up', 'up-left'], ['up', 'up-right'], ['left', 'up-left']... ]
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
BLUE = '\033[94m'
RED = '\033[91m'
END_COLOR = '\033[0m'


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
        self._files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        self._rows = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9}
        self._setup_squares()
        self._movable_squares = {'RED': [], 'BLUE': []}

        self._setup_squares()
        self._setup_pieces()

    def __str__(self):
        """
        String representation of a board. The box lines are drawn here, as well as the string representation of each
        square object comprising the board. Squares show as empty space unless a piece is on that square, in which case
        a color coded label for that piece is displayed instead. The fortress of one color's side is loosely outlined in
        its respective color.

        Board 'Squares' by index in self._squares list:
              a     b     c     d     e     f     g     h     i
           ┏━━━━━┯━━━━━┯━━━━━┍━━━━━┯━━━━━┯━━━━━┑━━━━━┯━━━━━┯━━━━━┓
         1 ┃  0  │  1  │  2  │  3  │  4  │  5  │  6  │  7  │  8  ┃
           ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨
         2 ┃  9  │ 10  │ 11  │ 12  │ 13  │ 14  │ 15  │ 16  │ 17  ┃
           ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨
         3 ┃ 18  │ 19  │ 20  │ 21  │ 22  │ 23  │ 24  │ 25  │ 26  ┃
           ┠─────┼─────┼─────└─────┴─────┴─────┘─────┼─────┼─────┨
         4 ┃ 27  │ 28  │ 29  │ 30  │ 31  │ 32  │ 33  │ 34  │ 35  ┃
           ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨
         5 ┃ 36  │ 37  │ 38  │ 39  │ 40  │ 41  │ 42  │ 43  │ 44  ┃
           ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨
         6 ┃ 45  │ 46  │ 47  │ 48  │ 49  │ 50  │ 51  │ 52  │ 53  ┃
           ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨
         7 ┃ 54  │ 55  │ 56  │ 57  │ 58  │ 59  │ 60  │ 61  │ 62  ┃
           ┠─────┼─────┼─────┌─────┬─────┬─────┐─────┼─────┼─────┨
         8 ┃ 63  │ 64  │ 65  │ 66  │ 67  │ 68  │ 69  │ 70  │ 71  ┃
           ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨
         9 ┃ 72  │ 73  │ 74  │ 75  │ 76  │ 77  │ 78  │ 79  │ 80  ┃
           ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨
         10┃ 81  │ 82  │ 83  │ 84  │ 85  │ 86  │ 87  │ 88  │ 89  ┃
           ┗━━━━━┷━━━━━┷━━━━━┕━━━━━┷━━━━━┷━━━━━┙━━━━━┷━━━━━┷━━━━━┛
        """
        rows = '      a     b     c     d     e     f     g     h     i\n'
        rows += f'   ┏━━━━━┯━━━━━┯━━━━━{RED}┍━━━━━┯━━━━━┯━━━━━┑{END_COLOR}━━━━━┯━━━━━┯━━━━━┓\n'
        labels = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10']
        for i in range(0, 90, 9):
            rows += ' ' + labels[i // 9] + '┃'
            rows += '│'.join(map(str, self._squares[i: i + 9]))
            rows += '┃\n'
            if i < 74:
                if i == 18:
                    rows += f'   ┠─────┼─────┼─────{RED}└─────┴─────┴─────┘{END_COLOR}─────┼─────┼─────┨\n'
                elif i == 54:
                    rows += f'   ┠─────┼─────┼─────{BLUE}┌─────┬─────┬─────┐{END_COLOR}─────┼─────┼─────┨\n'

                else:
                    rows += '   ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨\n'

        rows += f'   ┗━━━━━┷━━━━━┷━━━━━{BLUE}┕━━━━━┷━━━━━┷━━━━━┙{END_COLOR}━━━━━┷━━━━━┷━━━━━┛\n'
        return rows

    def _setup_squares(self):
        """
        Instantiates 90 square objects with row and file, and sets pointers to surrounding squares for each square.
        """
        for row in self._rows.keys():
            for file in self._files.keys():
                self._squares.extend([Square(file, row)])

        board = list(range(90))
        for index, square in enumerate(self._squares):
            if index - 1 in board:
                square.set_left(self._squares[index - 1])

            if index + 1 in board:
                square.set_right(self._squares[index + 1])

            if index - 9 in board:
                square.set_up(self._squares[index - 9])

            if index + 9 in board:
                square.set_down(self._squares[index + 9])

            if index - 10 in board:
                square.set_up_left(self._squares[index - 10])

            if index - 8 in board:
                square.set_up_right(self._squares[index - 8])

            if index + 8 in board:
                square.set_down_left(self._squares[index + 8])

            if index + 10 in board:
                square.set_down_right(self._squares[index + 10])

    def _setup_pieces(self):
        """Places pieces on board based on their starting board positions."""
        blue_map = self._pieces.get_blue_map().items()
        for piece, square_list in blue_map:
            for square_string in square_list:
                square_obj = self.get_square_from_string(square_string)
                square_obj.place_piece(piece)

        red_map = self._pieces.get_red_map().items()
        for piece, square_list in red_map:
            for square_string in square_list:
                square_obj = self.get_square_from_string(square_string)
                square_obj.place_piece(piece)

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

    def get_square_from_string(self, square_string):
        """Takes a string algebraic notation representation of a square, and returns the corresponding square object."""
        file = square_string[0]
        row = square_string[1:]
        index = 9 * self._rows[row] + self._files[file]
        return self._squares[index]


class Square:
    """
    A class representing a single Square on the game board. Each square has information about its row and file, and
    the piece on top of the square, if there is one.

    A Square has 8 pointers to surrounding squares, where pointers point to None for edge of board:

    ↖ ↑ ↗
    ← □ →
    ↙ ↓ ↘
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

    def __str__(self):
        if self._piece:
            return f'{self._piece}'
        else:
            return f'     '

    def get_piece(self):
        """
        Takes square object, e.g. 'a1', and returns the piece object on that square, otherwise returns None.

        :param  square: The square to retrieve the unit from
        :type   square: Square object
        """
        return self._piece

    def remove_piece(self):
        """Clears the square of any pieces."""
        pass

    def place_piece(self, piece):
        """
        Places a piece in the target square.

        :param  square: The square to set the piece on
        :type   square: Square object
        :param  piece:  The piece to set on the square
        :type   piece:  Piece object (could be any derived class of Piece - e.g. Horse, General, etc.)
        """
        self._piece = piece

    def get_string_of_square(self):
        """Returns a string representation of the coordinates of the square."""
        return f'{self._file}{self._row}'

    def set_up(self, square):
        """Takes Square object and sets pointer to square immediately above the current square."""
        self._up = square

    def get_up(self):
        """Returns Square object for square immediately above the current square."""
        return self._up

    def set_up_left(self, square):
        """Takes Square object and sets pointer to square immediately diagonal above-left the current square."""
        self._up_left = square

    def get_up_left(self):
        """Returns Square object for square immediately diagonal above-left current square."""
        return self._up_left

    def set_left(self, square):
        """Takes Square object and sets pointer to square immediately to the left of current square."""
        self._left = square

    def get_left(self):
        """Returns Square object for square immediately to the left of current square."""
        return self._left

    def set_down_left(self, square):
        """Takes Square object and sets pointer to square immediately diagonal below-left to current square."""
        self._down_left = square

    def get_down_left(self):
        """Returns Square object for square immediately diagonal below-left to current square."""
        return self._down_left

    def set_down(self, square):
        """Takes Square object and sets pointer to square immediately below current square."""
        self._down = square

    def get_down(self):
        """Returns Square object for square immediately below current square."""
        return self._down

    def set_down_right(self, square):
        """Takes Square object and sets pointer to square immediately diagonal below-right current square."""
        self._down_right = square

    def get_down_right(self):
        """Returns Square object for square immediately diagonal below-right current square."""
        return self._down_right

    def set_right(self, square):
        """Takes Square object and sets pointer to square immediately to the right of current square."""
        self._right = square

    def get_right(self):
        """Returns Square object for square immediately to the right of current square."""
        return self._down_right

    def set_up_right(self, square):
        """Takes Square object and sets pointer to square immediately diagonal above-right of current square."""
        self._up_right = square

    def get_up_right(self):
        """Returns Square object for square immediately diagonal above-right of current square."""
        return self._up_right


class PieceMap:
    """A class representing the location and interaction of game pieces."""

    def __init__(self):
        """Initializes a PieceMap class with starting positions for all pieces for each player."""
        self._blue_map = {
            General('BLUE'): ['e9'],
            Guard('BLUE'): ['d10', 'f10'],
            Horse('BLUE'): ['c10', 'h10'],
            Elephant('BLUE'): ['b10', 'g10'],
            Chariot('BLUE'): ['a10', 'i10'],
            Cannon('BLUE'): ['b8', 'h8'],
            Soldier('BLUE'): ['a7', 'c7', 'e7', 'g7', 'i7']
        }
        self._red_map = {
            General('RED'): ['e2'],
            Guard('RED'): ['d1', 'f1'],
            Horse('RED'): ['c1', 'h1'],
            Elephant('RED'): ['b1', 'g1'],
            Chariot('RED'): ['a1', 'i1'],
            Cannon('RED'): ['b3', 'h3'],
            Soldier('RED'): ['a4', 'c4', 'e4', 'g4', 'i4']
        }

    def set_piece_at(self, piece, square_to_add):
        """
        Takes a piece object and location, adds location for that piece on the PieceMap.

        :param  piece:  The piece whose locations are being updated
        :type   piece:  Piece object or child of Piece
        :param  square_to_add:  The new location of a moved piece
        :type   square_to_add:  Square object

        """
        pass

    def remove_piece_at(self, piece, square_to_remove):
        """
        Takes a piece object and location, removes location for that piece on the PieceMap.

        :param  piece:  The piece whose locations are being updated
        :type   piece:  Piece object or child of Piece
        :param  square_to_remove:   The previous location of a moved piece, OR the location of a taken piece
        :type   square_to_remove:   Square object
        """
        pass

    def get_blue_map(self):
        """Returns blue pieces and their locations."""
        return self._blue_map

    def get_red_map(self):
        """Returns red pieces and their locations."""
        return self._red_map


class PrintColors:
    """Class"""


class Piece:
    """Base class for all game pieces to be derived from."""

    def __init__(self, player):
        """Initializes the Piece base class. Stores the owning player as 'BLUE' or 'RED'."""
        self._player = player

    def get_player(self):
        """Returns the owning player of this piece."""
        return self._player


class General(Piece):
    """A class representing the General."""

    def __init__(self, player):
        """Initializes a General and its movement mechanism."""
        super().__init__(player)
        pass

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'BLUE':
            return f'{BLUE}★GEN★' + END_COLOR
        else:
            return f'{RED}★GEN★' + END_COLOR

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

    def __str__(self):
        """String representation of a guard for board printout."""
        if self._player == 'BLUE':
            return f'{BLUE}GUARD' + END_COLOR
        else:
            return f'{RED}GUARD' + END_COLOR

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

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'BLUE':
            return f'{BLUE}HORSE' + END_COLOR
        else:
            return f'{RED}HORSE' + END_COLOR

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

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'BLUE':
            return f'{BLUE} ELE ' + END_COLOR
        else:
            return f'{RED} ELE ' + END_COLOR

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

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'BLUE':
            return f'{BLUE} CHA ' + END_COLOR
        else:
            return f'{RED} CHA ' + END_COLOR

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

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'BLUE':
            return f'{BLUE} CAN ' + END_COLOR
        else:
            return f'{RED} CAN ' + END_COLOR

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

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'BLUE':
            return f'{BLUE} SOL ' + END_COLOR
        else:
            return f'{RED} SOL ' + END_COLOR

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        pass


if __name__ == '__main__':
    game = JanggiGame()
