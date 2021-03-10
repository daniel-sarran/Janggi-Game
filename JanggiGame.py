# Author:       Daniel Sarran
# Date:         TODO
# Description:  Korean chess game.

""" TODO LIST

LAST LEFT OFF ON:

    Chariot validate move & recursive traversal in ONE direction adding all squares along the way to "visited"
    - a recursive approach that iterates in each 4 directions
    - each new square is added in a direction, stops upon condition

 Movement:
 - Chariot (board and palace)
 - Cannon (board and palace)
 - General
 - Guard
 - Soldier (palace)

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
        # Check for player 'pass'
        if from_square == to_square:
            self._end_turn()
            return True

        # Validate move
        if not self._board.is_valid_move(from_square, to_square, self._turn):
            return False

        # Record move
        self._board.record_move(from_square, to_square)

        # Remove any captured piece - already done from movement
        # Update game state, if necessary

        # Update whose turn it is
        self._end_turn()
        return True

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

    def _end_turn(self):
        """Ends current player's turn."""
        if self._turn == 'BLUE':
            self._turn = 'RED'
        else:  # self._turn == 'RED'
            self._turn = 'BLUE'

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
        self._files = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        self._rows = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9}
        self._pieces = PieceMap()
        self._blue_palace = set()
        self._red_palace = set()
        self._palaces = set()

        self.setup()

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
        rows = '        a     b     c     d     e     f     g     h     i\n'
        rows += f'     ┏━━━━━┯━━━━━┯━━━━━{RED}┍━━━━━┯━━━━━┯━━━━━┑{END_COLOR}━━━━━┯━━━━━┯━━━━━┓\n'
        labels = ['1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ', '9 ', '10']
        for i in range(0, 90, 9):
            rows += '  ' + labels[i // 9] + ' ┃'
            rows += '│'.join(map(str, self._squares[i: i + 9]))
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

    def setup(self):
        """

        """
        self._setup_squares()
        self._setup_pieces()
        self._setup_palaces()

    def _setup_squares(self):
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

    def _setup_pieces(self):
        """Places pieces on board based on their starting board positions."""
        blue_map = self._pieces.get_piece_map_for('BLUE').items()
        for piece, square_list in blue_map:
            for square_string in square_list:
                square_obj = self.get_square_from_string(square_string)
                square_obj.place_piece(piece)

        red_map = self._pieces.get_piece_map_for('RED').items()
        for piece, square_list in red_map:
            for square_string in square_list:
                square_obj = self.get_square_from_string(square_string)
                square_obj.place_piece(piece)

    def _setup_palaces(self):
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

    def record_move(self, from_str, to_str):
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

    def get_square_from_string(self, square_string):
        """
        Takes a string algebraic notation representation of a square, and returns the corresponding square object.

        :param  square_string:  file (letter) goes first, row (number) goes second e.g. 'a1', 'i10'
        :type   square_string:  basestring
        """
        try:
            index = self.get_index_from_string(square_string)
            return self._squares[index]
        except InvalidSquareError:
            print('Invalid square entered')

    def get_index_from_string(self, square_string) -> int:
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

    def is_valid_move(self, from_str: str, to_str: str, player: str) -> bool:
        """
        Returns True if move is valid, False otherwise. Receives string representation of the 'from' and 'to' square,
        e.g. 'a1', 'b2'.
        """
        # Validate the squares are only a1 through i10
        try:
            from_square = self.get_square_from_string(from_str)
            self.get_square_from_string(to_str)
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

        # Compare 'to' against valid piece destination squares
        valid_moves = self._find_piece_movement_destinations(from_square)

        return to_str in valid_moves

    def _find_piece_movement_destinations(self, square_obj) -> list or None:
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
            valid_destinations = self.generate_general_guard_destinations(piece_obj, square_obj, player)

        elif piece_obj.get_type() == 'soldier':
            valid_destinations = self.generate_soldier_destinations(piece_obj, square_obj, player)

        elif piece_obj.get_type() == 'chariot':
            valid_destinations = self.generate_chariot_destinations(piece_obj, square_obj, player)

        elif piece_obj.get_type() == 'cannon':
            valid_destinations = self.generate_cannon_destinations(piece_obj, square_obj, player)

        else:  # horse, elephant
            for move_list in piece_obj.get_move_map():
                destination_square = self._valid_move_hor_ele(square_obj, 0, move_list, player, piece_obj)
                if destination_square:
                    valid_destinations.add(destination_square)

        return valid_destinations

    def generate_general_guard_destinations(self, piece_obj, square_obj, player):
        """

        :param piece_obj:
        :param square_obj:
        :param player:
        :return:
        """
        valid_destinations = set()

        for move_list in piece_obj.get_move_map():
            destination_square = self._valid_move_gua_gen(square_obj, 0, move_list, player, piece_obj)
            if destination_square:
                valid_destinations.add(destination_square)

        valid_destinations = valid_destinations.intersection(self._palaces)
        return valid_destinations

    def generate_soldier_destinations(self, piece_obj, square_obj, player):
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
        if square_obj.get_string_of_square() in self._palaces:

            move_map = piece_obj.get_palace_move_map()
            palace_destinations = set()

            for move_list in move_map:
                destination_square = self._valid_move_sol(square_obj, 0, move_list, player, piece_obj)
                if destination_square:
                    palace_destinations.add(destination_square)

            palace_destinations = palace_destinations.intersection(self._palaces)

        return valid_destinations.union(palace_destinations)

    # TODO: incomplete
    def generate_chariot_destinations(self, piece_obj, square_obj, player):
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
        if square_obj.get_string_of_square() in self._palaces:

            move_map = piece_obj.get_palace_move_map()
            palace_destinations = set()

            for direction in move_map:
                destination_squares = self._valid_move_cha(square_obj, direction, player, piece_obj)
                if destination_squares:
                    palace_destinations = palace_destinations.union(destination_squares)

            palace_destinations = palace_destinations.intersection(self._palaces)

        return valid_destinations.union(palace_destinations)

    # TODO: incomplete
    def generate_cannon_destinations(self, piece_obj, square_obj, player):
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
        if square_obj.get_string_of_square() in self._palaces:

            move_map = piece_obj.get_palace_move_map()
            palace_destinations = set()

            for direction in move_map:
                destination_squares = self._valid_move_can(square_obj, direction, player, piece_obj)
                if destination_squares:
                    palace_destinations = palace_destinations.union(destination_squares)

            palace_destinations = palace_destinations.intersection(self._palaces)

        return valid_destinations.union(palace_destinations)

    def generate_horse_elephant_destinations(self, piece_obj, square_obj, player):
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

    def _valid_move_cha(self, current_square, direction, player, piece, visited=False):
        """

        """
        # TODO
        if visited is False:
            visited = set()

        # Base case: out of bounds for board
        if current_square is None:
            return visited

        # Base case: palace movement out of palace
        if direction in piece.get_palace_move_map() and current_square.get_string_of_square() not in self._palaces:
            return

        if current_square.get_piece() and current_square.get_piece() is not piece:

            # Base case: end of movement -- blocked by ally
            if player == current_square.get_piece().get_player():
                return visited

            # Base case: end of movement -- enemy piece can be captured
            elif player != current_square.get_piece().get_player():
                visited.add(current_square.get_string_of_square())
                return visited

        # Empty space is a valid chariot move
        if not current_square.get_piece():
            visited.add(current_square.get_string_of_square())

        # Recursive case
        if direction == 'left':
            return self._valid_move_cha(current_square.get_left(), direction, player, piece, visited)

        elif direction == 'down_left':
            return self._valid_move_cha(current_square.get_down_left(), direction, player, piece, visited)

        elif direction == 'down':
            return self._valid_move_cha(current_square.get_down(), direction, player, piece, visited)

        elif direction == 'down_right':
            return self._valid_move_cha(current_square.get_down_right(), direction, player, piece, visited)

        elif direction == 'right':
            return self._valid_move_cha(current_square.get_right(), direction, player, piece, visited)

        elif direction == 'up_right':
            return self._valid_move_cha(current_square.get_up_right(), direction, player, piece, visited)

        elif direction == 'up':
            return self._valid_move_cha(current_square.get_up(), direction, player, piece, visited)

        elif direction == 'up_left':
            return self._valid_move_cha(current_square.get_up_left(), direction, player, piece, visited)

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
        if direction in piece.get_palace_move_map() and current_square.get_string_of_square() not in self._palaces:
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


class PieceMap:
    """A class representing the location and interaction of game pieces."""

    def __init__(self):
        """Initializes a PieceMap class with starting positions for all pieces for each player."""
        self._blue_map = {
            # General('BLUE'): ['e9'],
            # Guard('BLUE'): ['d10', 'f10'],
            # Horse('BLUE'): ['c10', 'h10'],
            # Elephant('BLUE'): ['b10', 'g10'],
            # Chariot('BLUE'): ['a10', 'i10'],
            # Cannon('BLUE'): ['b8', 'h8'],
            # Soldier('BLUE'): ['a7', 'c7', 'e7', 'g7', 'i7']
            Cannon('BLUE'): ['d10']
        }
        self._red_map = {
            # General('RED'): ['e2'],
            # Guard('RED'): ['d1', 'f1'],
            # Horse('RED'): ['c1', 'h1'],
            # Elephant('RED'): ['b1', 'g1'],
            # Chariot('RED'): ['a1', 'i1'],
            # Cannon('RED'): ['b3', 'h3'],
            # Soldier('RED'): ['a4', 'c4', 'e4', 'g4', 'i4']
            Cannon('RED'): ['d9'],
            Soldier('RED'): ['e9']

        }

        self._blue_locations = []
        for location_list in self._blue_map.values():
            self._blue_locations.extend(location_list)

        self._red_locations = []
        for location_list in self._red_map.values():
            self._red_locations.extend(location_list)

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

    def get_piece_map_for(self, player):
        """Returns a dictionary where keys are player's pieces and values are their locations."""
        if player == 'BLUE':
            return self._blue_map
        else:  # player == 'RED'
            return self._red_map

    def get_piece_locations_for(self, player):
        """Returns a list of all of a player's pieces' locations on the board in algebraic notation."""
        if player == 'BLUE':
            return self._blue_locations
        else:  # player == 'RED'
            return self._red_locations


class Piece:
    """Base class for all game pieces to be derived from."""

    def __init__(self, player):
        """Initializes the Piece base class. Stores the owning player as 'BLUE' or 'RED'."""
        self._player = player
        self._type = None
        self._move_map = None
        self._palace_move_map = None

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
            ['up_left', None],
            ['left', None],
            ['down_left', None],
            ['down', None],
            ['down_right', None],
            ['right', None],
            ['up_right', None]
        ]

    def __str__(self):
        """String representation of a general for board printout."""
        if self._player == 'BLUE':
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

    def __str__(self):
        """String representation of a guard for board printout."""
        if self._player == 'BLUE':
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
        if self._player == 'BLUE':
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
        if self._player == 'BLUE':
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
        if self._player == 'BLUE':
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
        if self._player == 'BLUE':
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
            'BLUE': [
                ['up', None],
                ['left', None],
                ['right', None]
            ],
            'RED': [
                ['down', None],
                ['left', None],
                ['right', None]
            ]
        }
        self._palace_move_map = {
            'BLUE': [
                ['up_right', None],
                ['up_left', None]
            ],
            'RED': [
                ['down_right', None],
                ['down_left', None]
            ]
        }

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
    game = JanggiGame()
    # square = game._board.get_square_from_string('d10')
    # piece = square.get_piece()
    # game._board.generate_cannon_destinations(piece, square, 'BLUE')
