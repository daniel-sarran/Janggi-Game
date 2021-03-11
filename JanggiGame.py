# Author:       Daniel Sarran
# Date:         TODO
# Description:  Korean chess game.

""" TODO LIST

LAST LEFT OFF ON:

 - Check & Checkmate
 - Follow general, follow palace squares

 Movement:
 - DONE!

 Put in "type" for each piece
 Remove move map from each class - moved to base Piece class
 Change blue map to list 'general' instead of the General class
    Will need to update setup pieces so that if 'general' -> General('BLUE')
 Check logic
 Checkmate logic
 
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
        self._move = self._board.get_move_object()
        self._turn = 'blue'
        self._game_state = 'UNFINISHED'

    def __repr__(self):
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
        rows = '        a     b     c     d     e     f     g     h     i\n'
        rows += f'     ┏━━━━━┯━━━━━┯━━━━━{RED}┍━━━━━┯━━━━━┯━━━━━┑{END_COLOR}━━━━━┯━━━━━┯━━━━━┓\n'
        labels = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10']
        for i in range(0, 90, 9):
            rows += '  ' + labels[i // 9] + ' ┃'
            rows += '│'.join(map(str, self._board._squares[i: i + 9]))
            rows += '┃\n'
            if i < 74:
                if i == 18:
                    rows += f'     ┠─────┼─────┼─────{RED}└─────┴─────┴─────┘{END_COLOR}─────┼─────┼─────┨\n'
                elif i == 54:
                    rows += f'     ┠─────┼─────┼─────{BLUE}┌─────┬─────┬─────┐{END_COLOR}─────┼─────┼─────┨\n'

                else:
                    rows += '     ┠─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┨\n'

        rows += f'     ┗━━━━━┷━━━━━┷━━━━━{BLUE}┕━━━━━┷━━━━━┷━━━━━┙{END_COLOR}━━━━━┷━━━━━┷━━━━━┛\n'
        return rows

    def get_game_state(self) -> str:
        """
        Returns a string of the current game state.
        Possible values are the strings "UNFINISHED", "RED_WON", or "BLUE_WON".
        """
        return self._game_state

    def set_game_state(self, state) -> None:
        """
        Takes in a string of current game state, updates game state to that state.

        :param  state    'UNFINISHED', 'BLUE_WON', 'RED_WON'
        :type   state     string
        """
        pass

    def make_move(self, from_square, to_square) -> bool:
        """
        Takes two string parameters of the square moved from and the square moved to.
        If the move is valid, updates game and piece board. A move to-and-from the same square is processed as a
        "pass" for that player. Checks for 'check' and 'checkmate', and records movement on game board and pieces.

        :param from_square  The source square the moving piece is coming from
        :type  from_square  Square object
        :param to_square    The source square the moving piece is coming from
        :type  to_square    Square object
        """
        print("make_move(", from_square, ",", to_square, ")")

        # Check if game is already over
        if self.get_game_state() != 'UNFINISHED':
            return False

        # Check for player 'pass'
        if from_square == to_square:
            self._end_turn()
            return True

        player = self._turn
        if player == 'blue':
            other_player = 'red'
        else:
            other_player = 'blue'

        # Validate move
        if not self._move.is_valid_move(from_square, to_square, player):
            return False

        # Record move
        to_square_obj = self._board.get_square_from_string(to_square)
        piece_obj = self._board.get_square_from_string(from_square).get_piece()
        self._move.update_piece_location(player, piece_obj, to_square_obj)
        self._board.record_move(from_square, to_square)

        # If in check after move, undo move
        if self.is_in_check(player):
            from_square_obj = self._board.get_square_from_string(from_square)
            piece_obj = self._board.get_square_from_string(to_square).get_piece()
            self._move.update_piece_location(player, piece_obj, from_square_obj)
            self._board.record_move(to_square, from_square)
            return False
        else:
            self._move.set_in_check(player, False)

        # Check / Checkmate other player
        self._move.update_attacks(player)
        self._move.update_attacks(other_player)
        if self.is_in_check(other_player):
            self._move.set_in_check(other_player, True)

        # Update game state, if necessary

        self._end_turn()
        return True

    def is_in_check(self, player: str) -> bool:
        """
        Takes a string representing the player. References whether the player's General's square is in the
        '_attacked' list of squares. If so, returns True. Otherwise, returns False.

        :param  player  One of the players 'blue' or 'red'
        :type   player  string
        """
        general_square = self._move.get_general_location_for(player)
        if general_square.get_string_of_square() in self._move.get_attacked_by(player):
            return True
        else:
            return False

    def _is_checkmate(self, player) -> bool:
        """
        Takes a string representing a player, returns a True if player is in checkmate, otherwise returns False.

        :param  player  One of the players 'blue' or 'red'
        :type   player  string
        """
        pass

    def _end_turn(self) -> None:
        """Ends current player's turn."""
        if self._turn == 'blue':
            self._turn = 'red'
        else:  # self._turn == 'red'
            self._turn = 'blue'

    def get_turn(self) -> str:
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
        self._files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        self._rows = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9}

        self._blue_palace = set()
        self._red_palace = set()
        self._palaces = set()
        self._palace_move_augmenting_squares = {
            'blue': {'d8', 'f8', 'e9', 'd10', 'f10'},
            'red': {'d1', 'f1', 'e2', 'd3', 'f3'}
        }
        self._starting_positions = {
            'blue': {
                'general': ['e9'],
                'guard': ['d10', 'f10'],
                'horse': ['c10', 'h10'],
                'elephant': ['b10', 'g10'],
                'chariot': ['a10', 'i10'],
                'cannon': ['b8', 'h8'],
                'soldier': ['a7', 'c7', 'e7', 'g7', 'i7']
            },
            'red': {
                'general': ['e2'],
                'guard': ['d1', 'f1'],
                'horse': ['c1', 'h1'],
                'elephant': ['b1', 'g1'],
                'chariot': ['a1', 'i1'],
                'cannon': ['b3', 'h3'],
                'soldier': ['a4', 'c4', 'e4', 'g4', 'i4']
            }
        }
        self._setup_squares()
        self._setup_palaces()
        self._move = Movement(self)
        self._setup_pieces()
        self._move.update_attacks('blue')
        self._move.update_attacks('red')

    def _setup_squares(self) -> None:
        """
        Instantiates 90 square objects with row and file, and sets pointers to surrounding squares for each square.
        """

        # Setup self._squares
        for row in self._rows.keys():
            for file in self._files.keys():
                self._squares.extend([Square(file, row)])

        for index, square in enumerate(self._squares):
            # Set left pointer, except for 'a' file squares
            if square.get_file() != 'a':
                square.set_left(self._squares[index - 1])

            # Set RIGHT pointer, except for 'i' file squares
            if square.get_file() != 'i':
                square.set_right(self._squares[index + 1])

            # Set UP pointer, except for '1' row squares
            if square.get_row() != '1':
                square.set_up(self._squares[index - 9])

            # Set DOWN pointer, except for '10' row squares
            if square.get_row() != '10':
                square.set_down(self._squares[index + 9])

            # Set UP_LEFT pointer, except for 'a' file squares and '1' row squares
            if square.get_file() != 'a' and square.get_row() != '1':
                square.set_up_left(self._squares[index - 10])

            # Set UP_RIGHT pointer, except for 'i' file squares and '1' row squares
            if square.get_file() != 'i' and square.get_row() != '1':
                square.set_up_right(self._squares[index - 8])

            # Set DOWN_LEFT pointer, except for 'a' file squares and '10' row squares
            if square.get_file() != 'a' and square.get_row() != '10':
                square.set_down_left(self._squares[index + 8])

            # Set DOWN_RIGHT pointer, except for 'i' file squares and '10' row squares
            if square.get_file() != 'i' and square.get_row() != '10':
                square.set_down_right(self._squares[index + 10])

    def _setup_palaces(self) -> None:
        """

        """
        self._red_palace = [
            file + row for file in list(self._files.keys())[3:6] for row in list(self._rows.keys())[:3]
        ]
        self._red_palace = set(self._red_palace)

        self._blue_palace = [
            file + row for file in list(self._files.keys())[3:6] for row in list(self._rows.keys())[7:]
        ]
        self._blue_palace = set(self._blue_palace)

        self._palaces = self._blue_palace.union(self._red_palace)

    def _setup_pieces(self) -> None:
        """Places pieces on board based on their starting board positions."""
        starting_positions = self._starting_positions
        for player in starting_positions:
            for piece, square_list in starting_positions[player].items():
                for square_string in square_list:
                    if piece == 'general':
                        piece_obj = General(player)
                    elif piece == 'guard':
                        piece_obj = Guard(player)
                    elif piece == 'horse':
                        piece_obj = Horse(player)
                    elif piece == 'elephant':
                        piece_obj = Elephant(player)
                    elif piece == 'chariot':
                        piece_obj = Chariot(player)
                    elif piece == 'cannon':
                        piece_obj = Cannon(player)
                    else:  # piece_obj == 'soldier'
                        piece_obj = Soldier(player)

                    square_obj = self.get_square_from_string(square_string)
                    square_obj.place_piece(piece_obj)
                    self._move.update_piece_location(player, piece_obj, square_obj)

    def record_move(self, from_str, to_str) -> None:
        """
        Finalizes movement of a piece from one square to another.

        :param  from_str: The source square the moving piece is coming from
        :type   from_str: string representing algebraic notation of square e.g. 'a1'
        :param  to_str:  The destination square the moving piece is moving to
        :type   to_str:  string representing algebraic notation of square e.g. 'a1'
        """
        from_square = self.get_square_from_string(from_str)
        to_square = self.get_square_from_string(to_str)
        to_square.place_piece(from_square.get_piece())
        from_square.remove_piece()

    def get_square_from_string(self, square_string: str):
        """
        Takes a string algebraic notation representation of a square, and returns the corresponding square object.

        :param  square_string:  file (letter) goes first, row (number) goes second e.g. 'a1', 'i10'
        :type   square_string:  basestring
        """
        try:
            index = self._get_index_from_string(square_string)
            return self._squares[index]
        except InvalidSquareError:
            print('Invalid square entered')

    def _get_index_from_string(self, square_string: str) -> int:
        """
        Takes a string algebraic notation representation of a square, and returns the corresponding index of the square
        in self._squares.

        :param  square_string:  file (letter) goes first, row (number) goes second e.g. 'a1', 'i10'
        :type   square_string:  basestring
        """
        # Not a proper file
        if square_string[0] not in self._files.keys():
            raise InvalidSquareError

        # Not a proper row
        if square_string[1:] not in self._rows.keys():
            raise InvalidSquareError

        file = square_string[0]
        row = square_string[1:]

        index = 9 * self._rows[row] + self._files[file]
        return index

    def get_palace(self, player):
        """

        :param player:
        :return:
        """
        if player == 'blue':
            return self._blue_palace
        else:  # player == 'RED'
            return self._red_palace

    def get_palaces(self):
        """

        :return:
        """
        return self._palaces

    def get_palace_move_augmenting_squares(self, player):
        """

        :return:
        """
        return self._palace_move_augmenting_squares[player]

    def get_move_object(self):
        """

        :return:
        """
        return self._move


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
        """

        :return:
        """
        if self._piece:
            return f'{self._piece}'
        else:
            return f'     '

    def __repr__(self):
        """

        :return:
        """
        return f'<{self._file}{self._row}>'

    def get_piece(self):
        """Takes square object, e.g. 'a1', and returns the piece object on that square, otherwise returns None."""
        return self._piece

    def remove_piece(self):
        """Clears the square of any pieces."""
        self._piece = None

    def place_piece(self, piece):
        """
        Places a piece in the target square.

        :param  piece:  The piece to set on the square
        :type   piece:  Piece object (could be any derived class of Piece - e.g. Horse, General, etc.)
        """
        self._piece = piece

    def get_string_of_square(self):
        """Returns a string representation of the coordinates of the square."""
        return f'{self._file}{self._row}'

    def get_file(self):
        """Returns the file of the current square."""
        return self._file

    def get_row(self):
        """Returns the row of the current square."""
        return self._row

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
        return self._right

    def set_up_right(self, square):
        """Takes Square object and sets pointer to square immediately diagonal above-right of current square."""
        self._up_right = square

    def get_up_right(self):
        """Returns Square object for square immediately diagonal above-right of current square."""
        return self._up_right


class Movement:
    """A class representing the location and interaction of game pieces."""

    def __init__(self, board_obj):
        """Initializes a PieceMap class with starting positions for all pieces for each player."""
        self._board = board_obj
        # attacks = {PLAYER: {SQUARE object: {destination strings e.g. 'a1', 'a2'}}}
        self._attacks = {
            'blue': dict(),
            'red': dict()
        }
        # attacked_by = {'blue': {'a1': SQUARE object}} -- 'a1' is attacked by the square object
        self._attacked_by = {
            'blue': dict(),
            'red': dict()
        }
        self._pieces_locations = {
            'blue': dict(),
            'red': dict()
        }
        self._generals = {
            'blue': self._board.get_square_from_string('e9'),
            'red': self._board.get_square_from_string('e2')
        }
        self._in_check = {
            'blue': False,
            'red': False
        }

    # TODO: instead of generating moves, see if it is in the player's piece attacks
    def is_valid_move(self, from_str: str, to_str: str, player: str) -> bool:
        """
        Returns True if move is valid, False otherwise. Receives string representation of the 'from' and 'to' square,
        e.g. 'a1', 'b2'.
        """
        # Validate the squares are only a1 through i10
        try:
            from_square = self._board.get_square_from_string(from_str)
            self._board.get_square_from_string(to_str)
        except InvalidSquareError:
            print('Invalid Square - enter squares from "a1" to "i10"')
            return False

        piece = from_square.get_piece()

        # There is no piece on the 'from' square
        if not piece:
            return False

        # Piece does not belong to player with active turn
        if player != piece.get_player():
            return False

        if player == 'blue':
            other_player = 'red'
        else:
            other_player = 'blue'

        from_square = self._board.get_square_from_string(from_str)
        return to_str in self._attacks[player][from_square]

    def update_piece_location(self, player, piece_obj, square_obj):
        """

        :param player:
        :param square_obj:
        :param piece_obj:
        :return:
        """
        if piece_obj.get_type() == 'general':
            self._generals[player] = square_obj
        self._pieces_locations[player][piece_obj] = square_obj

    def update_attacks(self, player_turn):
        """

        :return:
        """
        if player_turn == 'blue':
            other_player = 'red'
        else:  # player == 'red'
            other_player = 'blue'

        self._attacks[player_turn] = dict()
        self._attacked_by[other_player] = dict()

        # update attacks/movable squares for current player's pieces
        for piece_obj, square_obj in self._pieces_locations[player_turn].items():
            self._attacks[player_turn][square_obj] = self._find_piece_movement_destinations(square_obj)

            # update map of other player's squares being attacked
            for possible_destination in self._attacks[player_turn][square_obj]:

                if possible_destination not in self._attacked_by[other_player]:
                    self._attacked_by[other_player][possible_destination] = {square_obj}
                else:
                    self._attacked_by[other_player][possible_destination].add(square_obj)

    def get_general_location_for(self, player) -> Square:
        """

        :param player:
        :return:
        """
        return self._generals[player]

    def get_attacks(self, player, ) -> dict:
        """

        :param square_obj:
        :return:
        """
        return self._attacks[player]

    def get_attacked_by(self, player):
        """

        :param player:
        :return:
        """
        return self._attacked_by[player]

    def set_in_check(self, player, boolean):
        """

        :param boolean:
        :param player:
        :return:
        """
        self._in_check[player] = boolean

    def _find_piece_movement_destinations(self, square_obj) -> set or None:
        """
        Receives a Square object holding a game piece owned by the player whose turn it is. Returns a list of possible
        destination squares based on the piece's movement, and other pieces on the board (e.g. collision or capture).

        Since this method receives a Square object, it is assumed the square has been previously validated. Utilizes
        a set of helper methods specific to each piece to calculate possible moves.

        It is also assumed the player who owns the piece has been previously validated as the active player.

        :param square_obj:
        """
        piece_obj = square_obj.get_piece()

        if not piece_obj:
            return

        player = piece_obj.get_player()
        valid_destinations = set()

        if piece_obj.get_type() == 'guard' or piece_obj.get_type() == 'general':
            valid_destinations = self._generate_general_guard_destinations(piece_obj, square_obj, player)

        elif piece_obj.get_type() == 'soldier':
            valid_destinations = self._generate_soldier_destinations(piece_obj, square_obj, player)

        elif piece_obj.get_type() == 'chariot':
            valid_destinations = self._generate_chariot_destinations(piece_obj, square_obj, player)

        elif piece_obj.get_type() == 'cannon':
            valid_destinations = self._generate_cannon_destinations(piece_obj, square_obj, player)

        else:  # horse, elephant
            for move_list in piece_obj.get_move_map():
                destination_square = self._valid_move_hor_ele(square_obj, 0, move_list, player, piece_obj)
                if destination_square:
                    valid_destinations.add(destination_square)

        return valid_destinations

    def _generate_general_guard_destinations(self, piece_obj, square_obj, player) -> set:
        """

        :param piece_obj:
        :param square_obj:
        :param player:
        :return:
        """
        valid_destinations = set()
        diagonal_destinations = set()

        for move_list in piece_obj.get_move_map():
            destination_square = self._valid_move_gua_gen(square_obj, 0, move_list, player, piece_obj)
            if destination_square:
                valid_destinations.add(destination_square)

        # Find valid square destinations (include palace movement augmentation)
        if square_obj.get_string_of_square() in self._board.get_palace_move_augmenting_squares(player):

            move_map = piece_obj.get_palace_move_map()
            palace_destinations = set()

            for move_list in move_map:
                destination_square = self._valid_move_gua_gen(square_obj, 0, move_list, player, piece_obj)
                if destination_square:
                    palace_destinations.add(destination_square)

            diagonal_destinations = palace_destinations.intersection(self._board.get_palace(player))

        valid_destinations = valid_destinations.union(diagonal_destinations)
        valid_destinations = valid_destinations.intersection(self._board.get_palace(player))

        return valid_destinations

    def _generate_soldier_destinations(self, piece_obj, square_obj, player):
        """

        :param piece_obj:
        :param square_obj:
        :param player:
        :return:
        """
        valid_destinations = set()
        palace_destinations = set()

        move_map = piece_obj.get_move_map()

        # Find valid square destinations (non-palace movement)
        for move_list in move_map:
            destination_square = self._valid_move_sol(square_obj, 0, move_list, player, piece_obj)
            if destination_square:
                valid_destinations.add(destination_square)

        # Find valid square destinations (include palace movement augmentation)
        if square_obj.get_string_of_square() in self._board.get_palace_move_augmenting_squares(player):

            move_map = piece_obj.get_palace_move_map()
            palace_destinations = set()

            for move_list in move_map:
                destination_square = self._valid_move_sol(square_obj, 0, move_list, player, piece_obj)
                if destination_square:
                    palace_destinations.add(destination_square)

            palace_destinations = palace_destinations.intersection(self._board.get_palaces())

        return valid_destinations.union(palace_destinations)

    def _generate_chariot_destinations(self, piece_obj, square_obj, player):
        """

        :param piece_obj:
        :param square_obj:
        :param player:
        :return:
        """
        valid_destinations = set()
        palace_destinations = set()

        move_map = piece_obj.get_move_map()

        # Find valid square destinations (non-palace movement)
        for direction in move_map:
            destination_squares = self._valid_move_cha(square_obj, direction, player, piece_obj)
            if destination_squares:
                valid_destinations = valid_destinations.union(destination_squares)

        # Find valid square destinations (include palace movement augmentation)
        if square_obj.get_string_of_square() in self._board.get_palace_move_augmenting_squares(player):

            move_map = piece_obj.get_palace_move_map()
            palace_destinations = set()

            for direction in move_map:
                destination_squares = self._valid_move_cha(square_obj, direction, player, piece_obj)
                if destination_squares:
                    palace_destinations = palace_destinations.union(destination_squares)

            palace_destinations = palace_destinations.intersection(self._board.get_palaces())

        return valid_destinations.union(palace_destinations)

    def _generate_cannon_destinations(self, piece_obj, square_obj, player):
        """

        :param piece_obj:
        :param square_obj:
        :param player:
        :return:
        """
        valid_destinations = set()
        palace_destinations = set()

        move_map = piece_obj.get_move_map()

        # Find valid square destinations (non-palace movement)
        for direction in move_map:
            destination_squares = self._valid_move_can(square_obj, direction, player, piece_obj)
            if destination_squares:
                valid_destinations = valid_destinations.union(destination_squares)

        # Find valid square destinations (include palace movement augmentation)
        if square_obj.get_string_of_square() in self._board.get_palace_move_augmenting_squares(player):

            move_map = piece_obj.get_palace_move_map()
            palace_destinations = set()

            for direction in move_map:
                destination_squares = self._valid_move_can(square_obj, direction, player, piece_obj)
                if destination_squares:
                    palace_destinations = palace_destinations.union(destination_squares)

            palace_destinations = palace_destinations.intersection(self._board.get_palaces())

        return valid_destinations.union(palace_destinations)

    def _generate_horse_elephant_destinations(self, piece_obj, square_obj, player):
        """

        :param piece_obj:
        :param square_obj:
        :param player:
        :return:
        """
        valid_destinations = set()

        for move_list in piece_obj.get_move_map():
            destination_square = self._valid_move_sol(square_obj, 0, move_list, player, piece_obj)
            if destination_square:
                valid_destinations.add(destination_square)

        return valid_destinations

    def _valid_move_gua_gen(self, current_square, index, move_list, player, piece):
        """

        :param current_square:
        :param index:
        :param move_list:
        :param player:
        :param piece:
        :return:
        """
        # Base case: out of palace
        if current_square is None:
            return

        # Base case: friendly piece found
        next_move = move_list[index]

        if current_square.get_piece() and next_move is not None:
            if (player == current_square.get_piece().get_player() and
                    current_square.get_piece() is not piece):
                return
            elif player != current_square.get_piece().get_player():
                return

        # Base case: end of movement, destination is valid
        if next_move is None:
            if current_square.get_piece():
                if player == current_square.get_piece().get_player():
                    return
                elif player != current_square.get_piece().get_player():
                    return current_square.get_string_of_square()
            else:
                return current_square.get_string_of_square()

        # Recursive case
        if next_move == 'left':
            return self._valid_move_sol(current_square.get_left(), index + 1, move_list, player, piece)

        elif next_move == 'down_left':
            return self._valid_move_sol(current_square.get_down_left(), index + 1, move_list, player, piece)

        elif next_move == 'down':
            return self._valid_move_sol(current_square.get_down(), index + 1, move_list, player, piece)

        elif next_move == 'down_right':
            return self._valid_move_sol(current_square.get_down_right(), index + 1, move_list, player, piece)

        elif next_move == 'right':
            return self._valid_move_sol(current_square.get_right(), index + 1, move_list, player, piece)

        elif next_move == 'up_right':
            return self._valid_move_sol(current_square.get_up_right(), index + 1, move_list, player, piece)

        elif next_move == 'up':
            return self._valid_move_sol(current_square.get_up(), index + 1, move_list, player, piece)

        elif next_move == 'up_left':
            return self._valid_move_sol(current_square.get_up_left(), index + 1, move_list, player, piece)

    def _valid_move_hor_ele(self, current_square, index, move_list, player, piece):
        """

        :param current_square:
        :param index:
        :param move_list:
        :param player:
        :param piece:
        :return:
        """
        # Base case: out of bounds for board
        if current_square is None:
            return

        next_move = move_list[index]

        # Base case: movement is blocked
        if current_square.get_piece() and next_move is not None:
            if (player == current_square.get_piece().get_player() and
                    current_square.get_piece() is not piece):
                return
            elif player != current_square.get_piece().get_player():
                return

        # Base case: final square in movement is reached
        if next_move is None:
            if current_square.get_piece():
                if player == current_square.get_piece().get_player():
                    return
                elif player != current_square.get_piece().get_player():
                    return current_square.get_string_of_square()
            else:
                return current_square.get_string_of_square()

        # Recursive case
        if next_move == 'left':
            return self._valid_move_hor_ele(current_square.get_left(), index + 1, move_list, player, piece)

        elif next_move == 'down_left':
            return self._valid_move_hor_ele(current_square.get_down_left(), index + 1, move_list, player, piece)

        elif next_move == 'down':
            return self._valid_move_hor_ele(current_square.get_down(), index + 1, move_list, player, piece)

        elif next_move == 'down_right':
            return self._valid_move_hor_ele(current_square.get_down_right(), index + 1, move_list, player, piece)

        elif next_move == 'right':
            return self._valid_move_hor_ele(current_square.get_right(), index + 1, move_list, player, piece)

        elif next_move == 'up_right':
            return self._valid_move_hor_ele(current_square.get_up_right(), index + 1, move_list, player, piece)

        elif next_move == 'up':
            return self._valid_move_hor_ele(current_square.get_up(), index + 1, move_list, player, piece)

        elif next_move == 'up_left':
            return self._valid_move_hor_ele(current_square.get_up_left(), index + 1, move_list, player, piece)

    def _valid_move_cha(self, current_square, direction, player, piece, destinations=False):
        """

        """
        # Instantiate the destinations set on first recursive call
        if destinations is False:
            destinations = set()

        # Base case: out of bounds for board
        if current_square is None:
            return destinations

        # Base case: palace movement out of palace
        if (direction in piece.get_palace_move_map() and
                current_square.get_string_of_square() not in self._board.get_palaces()):
            return

        if current_square.get_piece() and current_square.get_piece() is not piece:

            # Base case: end of movement -- blocked by ally
            if player == current_square.get_piece().get_player():
                return destinations

            # Base case: end of movement -- enemy piece can be captured
            elif player != current_square.get_piece().get_player():
                destinations.add(current_square.get_string_of_square())
                return destinations

        # Empty space is a valid chariot move
        if not current_square.get_piece():
            destinations.add(current_square.get_string_of_square())

        # Recursive case
        if direction == 'left':
            return self._valid_move_cha(current_square.get_left(), direction, player, piece, destinations)

        elif direction == 'down_left':
            return self._valid_move_cha(current_square.get_down_left(), direction, player, piece, destinations)

        elif direction == 'down':
            return self._valid_move_cha(current_square.get_down(), direction, player, piece, destinations)

        elif direction == 'down_right':
            return self._valid_move_cha(current_square.get_down_right(), direction, player, piece, destinations)

        elif direction == 'right':
            return self._valid_move_cha(current_square.get_right(), direction, player, piece, destinations)

        elif direction == 'up_right':
            return self._valid_move_cha(current_square.get_up_right(), direction, player, piece, destinations)

        elif direction == 'up':
            return self._valid_move_cha(current_square.get_up(), direction, player, piece, destinations)

        elif direction == 'up_left':
            return self._valid_move_cha(current_square.get_up_left(), direction, player, piece, destinations)

    def _valid_move_can(self, current_square, direction, player, piece, destinations=False, pieces_in_path=0):
        """

        :param current_square:
        :param direction:
        :param player:
        :param piece:
        :param pieces_in_path:
        :return:
        """
        if destinations is False:
            destinations = set()

        # Base case: out of bounds for board
        if current_square is None:
            return destinations

        # Base case: augmented palace movement is out of palace zone
        if (direction in piece.get_palace_move_map() and
                current_square.get_string_of_square() not in self._board.get_palaces()):
            return destinations

        # Before jump, found piece in path
        if pieces_in_path == 0 and current_square.get_piece():

            # Base case: cannot jump over cannon
            if current_square.get_piece().get_type() == 'cannon' and current_square.get_piece() is not piece:
                return destinations

            # Jump activated: first blocking piece found
            if current_square.get_piece() is not piece:
                pieces_in_path = 1

        # After jump
        elif pieces_in_path == 1:

            # Empty squares after jump are valid cannon destinations
            if not current_square.get_piece():
                destinations.add(current_square.get_string_of_square())

            # Occupied squares after jump
            elif current_square.get_piece():

                # Occupied square is another cannon
                if current_square.get_piece().get_type() == 'cannon':
                    return destinations

                # Ally piece
                elif current_square.get_piece().get_player() == player:
                    return destinations

                # Enemy piece, valid destination and end of movement
                elif current_square.get_piece().get_player() != player:
                    destinations.add(current_square.get_string_of_square())
                    return destinations

        # Recursive case
        if direction == 'left':
            return self._valid_move_can(current_square.get_left(), direction, player, piece, destinations,
                                        pieces_in_path)

        elif direction == 'down_left':
            return self._valid_move_can(current_square.get_down_left(), direction, player, piece, destinations,
                                        pieces_in_path)

        elif direction == 'down':
            return self._valid_move_can(current_square.get_down(), direction, player, piece, destinations,
                                        pieces_in_path)

        elif direction == 'down_right':
            return self._valid_move_can(current_square.get_down_right(), direction, player, piece, destinations,
                                        pieces_in_path)

        elif direction == 'right':
            return self._valid_move_can(current_square.get_right(), direction, player, piece, destinations,
                                        pieces_in_path)

        elif direction == 'up_right':
            return self._valid_move_can(current_square.get_up_right(), direction, player, piece, destinations,
                                        pieces_in_path)

        elif direction == 'up':
            return self._valid_move_can(current_square.get_up(), direction, player, piece, destinations,
                                        pieces_in_path)

        elif direction == 'up_left':
            return self._valid_move_can(current_square.get_up_left(), direction, player, piece, destinations,
                                        pieces_in_path)

    def _valid_move_sol(self, current_square, index, move_list, player, piece):
        """

        :param current_square:
        :param index:
        :param move_list:
        :param player:
        :param piece:
        :return:
        """
        # Base case: out of bounds for board
        if current_square is None:
            return

        # Base case: friendly piece found
        next_move = move_list[index]

        if current_square.get_piece() and next_move is not None:
            if (player == current_square.get_piece().get_player() and
                    current_square.get_piece() is not piece):
                return
            elif player != current_square.get_piece().get_player():
                return

        # Base case: end of movement, destination is valid
        if next_move is None:
            if current_square.get_piece():
                if player == current_square.get_piece().get_player():
                    return
                elif player != current_square.get_piece().get_player():
                    return current_square.get_string_of_square()
            else:
                return current_square.get_string_of_square()

        # Recursive case
        if next_move == 'left':
            return self._valid_move_sol(current_square.get_left(), index + 1, move_list, player, piece)

        elif next_move == 'down_left':
            return self._valid_move_sol(current_square.get_down_left(), index + 1, move_list, player, piece)

        elif next_move == 'down':
            return self._valid_move_sol(current_square.get_down(), index + 1, move_list, player, piece)

        elif next_move == 'down_right':
            return self._valid_move_sol(current_square.get_down_right(), index + 1, move_list, player, piece)

        elif next_move == 'right':
            return self._valid_move_sol(current_square.get_right(), index + 1, move_list, player, piece)

        elif next_move == 'up_right':
            return self._valid_move_sol(current_square.get_up_right(), index + 1, move_list, player, piece)

        elif next_move == 'up':
            return self._valid_move_sol(current_square.get_up(), index + 1, move_list, player, piece)

        elif next_move == 'up_left':
            return self._valid_move_sol(current_square.get_up_left(), index + 1, move_list, player, piece)


class Piece:
    """Base class for all game pieces to be derived from."""

    def __init__(self, player):
        """Initializes the Piece base class. Stores the owning player as 'blue' or 'red'."""
        self._player = player
        self._type = None
        self._move_map = None
        self._palace_move_map = None

    def __repr__(self):
        """

        :return:
        """
        return f'<{self._player} {self._type}>'

    def get_player(self):
        """Returns the owning player of this piece."""
        return self._player

    def get_type(self):
        """Returns the type data member of this piece."""
        return self._type

    def get_move_map(self):
        """
        Returns the possible movements of a Janggi piece. The move map is a list of possible moves.
        Each move will iterate the direction one square at a time, by comma delineation.
        """
        return self._move_map

    def get_palace_move_map(self):
        """

        :return:
        """
        return self._palace_move_map


class General(Piece):
    """A class representing the General."""

    def __init__(self, player):
        """Initializes a General and its movement mechanism."""
        super().__init__(player)
        self._type = 'general'
        self._move_map = [
            ['up', None],
            ['left', None],
            ['down', None],
            ['right', None],
        ]
        self._palace_move_map = [
            ['up_left', None],
            ['down_left', None],
            ['down_right', None],
            ['up_right', None]
        ]

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'blue':
            return f'{BLUE}★GEN★' + END_COLOR
        else:
            return f'{RED}★GEN★' + END_COLOR


class Guard(Piece):
    """A class representing a Guard."""

    def __init__(self, player):
        """Initializes a Guard and its movement mechanism."""
        super().__init__(player)
        self._type = 'guard'
        self._move_map = [
            ['up', None],
            ['up_left', None],
            ['left', None],
            ['down_left', None],
            ['down', None],
            ['down_right', None],
            ['right', None],
            ['up_right', None]
        ]
        self._palace_move_map = [
            ['up_left', None],
            ['down_left', None],
            ['down_right', None],
            ['up_right', None]
        ]

    def __str__(self):
        """String representation of a guard for board printout."""
        if self._player == 'blue':
            return f'{BLUE}GUARD' + END_COLOR
        else:
            return f'{RED}GUARD' + END_COLOR


class Horse(Piece):
    """A class representing a Horse."""

    def __init__(self, player):
        """Initializes a Horse and its movement mechanism."""
        super().__init__(player)
        self._type = 'horse'
        self._move_map = [
            ['up', 'up_left', None],
            ['up', 'up_right', None],
            ['left', 'up_left', None],
            ['left', 'down_left', None],
            ['right', 'up_right', None],
            ['right', 'down_right', None],
            ['down', 'down_left', None],
            ['down', 'down_right', None]
        ]

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'blue':
            return f'{BLUE}HORSE' + END_COLOR
        else:
            return f'{RED}HORSE' + END_COLOR


class Elephant(Piece):
    """A class representing an elephant."""

    def __init__(self, player):
        """Initializes an Elephant and its movement mechanism."""
        super().__init__(player)
        self._type = 'elephant'
        self._move_map = [
            ['up', 'up_left', 'up_left', None],
            ['up', 'up_right', 'up_right', None],
            ['left', 'up_left', 'up_left', None],
            ['left', 'down_left', 'down_left', None],
            ['right', 'up_right', 'up_right', None],
            ['right', 'down_right', 'down_right', None],
            ['down', 'down_left', 'down_left', None],
            ['down', 'down_right', 'down_right', None]
        ]

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'blue':
            return f'{BLUE} ELE ' + END_COLOR
        else:
            return f'{RED} ELE ' + END_COLOR


class Chariot(Piece):
    """A class representing a Chariot."""

    def __init__(self, player):
        """Initializes a Chariot and its movement mechanism."""
        super().__init__(player)
        self._type = 'chariot'
        self._move_map = [
            'up',
            'down',
            'left',
            'right'
        ]
        self._palace_move_map = [
            'up_left',
            'up_right',
            'down_left',
            'down_right'
        ]

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'blue':
            return f'{BLUE} CHA ' + END_COLOR
        else:
            return f'{RED} CHA ' + END_COLOR


class Cannon(Piece):
    """A class representing a Cannon."""

    def __init__(self, player):
        """Initializes a Cannon and its movement mechanism."""
        super().__init__(player)
        self._type = 'cannon'
        self._move_map = [
            'up',
            'down',
            'left',
            'right'
        ]
        self._palace_move_map = [
            'up_left',
            'up_right',
            'down_left',
            'down_right'
        ]

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'blue':
            return f'{BLUE} CAN ' + END_COLOR
        else:
            return f'{RED} CAN ' + END_COLOR


class Soldier(Piece):
    """A class representing a Soldier."""

    def __init__(self, player):
        """Initializes a Soldier and its movement mechanism."""
        super().__init__(player)
        self._type = 'soldier'
        self._move_map = {
            'blue': [
                ['up', None],
                ['left', None],
                ['right', None]
            ],
            'red': [
                ['down', None],
                ['left', None],
                ['right', None]
            ]
        }
        self._palace_move_map = {
            'blue': [
                ['up_right', None],
                ['up_left', None]
            ],
            'red': [
                ['down_right', None],
                ['down_left', None]
            ]
        }

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'blue':
            return f'{BLUE} SOL ' + END_COLOR
        else:
            return f'{RED} SOL ' + END_COLOR

    def get_move_map(self):
        """
        Returns a list of 'move lists'. The 'move lists' are stepwise movements from one square to another that when
        completed properly move the piece along the correct path.
        """
        return self._move_map[self._player]

    def get_palace_move_map(self):
        """
        Returns a list of 'move lists' specifically within the fortress. The 'move lists' are stepwise movements from
        one square to another that when completed properly move the piece along the correct path.
        """
        return self._palace_move_map[self._player]


class InvalidSquareError(Exception):
    """Exception that gets thrown when an invalid square string representation is passed."""
    pass


if __name__ == '__main__':
    # pass
    game = JanggiGame()
    game.make_move('e9', 'f8')
    game.make_move('e2', 'f3')
