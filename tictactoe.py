import math
import random
 
class TicTacToe:
    """
    a class for the TicTacToe game
    """
    def __init__(self, board_size=3, win_length=3):
        self.EMPTY_SPOT = 0
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.type_to_display = {
            self.EMPTY_SPOT: ' ',
            self.PLAYER_PIECE: 'X',
            self.AI_PIECE: 'O'
        }

        self.board_size = board_size
        self.num_positions = board_size * board_size
        self.board = [self.EMPTY_SPOT] * self.num_positions
        self.win_length = win_length

    def display(self, input_list):
        assert len(input_list) == self.num_positions
        for row in xrange(self.board_size):
            start_pos = row * self.board_size
            end_pos = start_pos + self.board_size
            row_str = '|'.join(map(str, input_list[start_pos:end_pos]))
            print row_str
 
    def display_movement(self):
        print "Movement Key:"
        self.display(range(1, self.num_positions+1))
 
    def display_board(self):
        print "Board:"
        input = [self.type_to_display[piece] for piece in self.board]
        self.display(input)
 
    def index2position(self, index):
        assert isinstance(index, int)
        if not (0 <= index <= self.num_positions-1):
            # invalid index
            return -1, -1
        row = index / self.board_size
        col = index % self.board_size
        return row, col
 
    def position2index(self, row, col):
        assert isinstance(row, int)
        assert isinstance(col, int)
        if row < 0 or row >= self.board_size or \
            col < 0 or col >= self.board_size:
            # invalid row or col
            return -1
        return row * self.board_size + col
 
    def get_position(self):
        try:
            index = int(raw_input("Where to? "))
        except ValueError:
            print "invalid movement key"
            return self.get_position()
 
        index -= 1
        if not (0 <= index <= self.num_positions-1):
            print "movement key out of range"
            return self.get_position()
        elif self.board[index] != self.EMPTY_SPOT:
            print "position already taken"
            return self.get_position()
        else:
            return index
 
    def ai_move(self, debug=False):
        # squared scores work better
        gain = map(lambda x: x*x, self.compute_scores(piece_type=self.AI_PIECE))
        risk = map(lambda x: x*x, self.compute_scores(piece_type=self.PLAYER_PIECE))
        scores = [gain[idx] + risk[idx] for idx in xrange(len(gain))]
        if debug:
            print "potential gain:"
            self.display(gain)
            print "potential risk:"
            self.display(risk)
            print "move scores:"
            self.display(scores)
 
        max_score = max(scores)
        max_idx = [index for index in xrange(len(scores))
                        if scores[index] == max_score and self.board[index] == self.EMPTY_SPOT]
        if len(max_idx) > 0:
            idx = random.choice(max_idx)
        else:
            # no available moves, it's a draw
            return None
        print "I will put an O at position %d" % idx
        self.place_piece(idx, self.AI_PIECE)
        if self.is_game_over(idx, self.AI_PIECE):
            return True     # ai wins
        else:
            return False

    def player_move(self, idx):
        self.place_piece(idx, self.PLAYER_PIECE)
 
    def place_piece(self, index, piece_type):
        assert isinstance(index, int)
        assert isinstance(piece_type, int)
        assert piece_type in (self.PLAYER_PIECE, self.AI_PIECE)
        if self.board[index] != self.EMPTY_SPOT:
            print("position %d already taken" % index)
            return False
        else:
            self.board[index] = piece_type
            self.display_board()
            return True
 
    def is_game_over(self, index, piece_type):
        if self.compute_score(index, piece_type) >= self.win_length:
             return True
        else:
             return False
 
    def compute_scores(self, piece_type):
        scores = []
        for index in xrange(self.num_positions):
            if self.board[index] == self.EMPTY_SPOT:
                scores.append(self.compute_score(index, piece_type))
            else:
                scores.append(0)
        return scores
 
    def compute_score(self, index, piece_type):
        if piece_type == self.EMPTY_SPOT:
            piece_type = self.board[index]
        # checking 8 directions
        # ul, u, ur, r, dr, d, dl, l
        ul = self.check_one_direction(index, -1, -1, piece_type)
        u  = self.check_one_direction(index, -1,  0, piece_type)
        ur = self.check_one_direction(index, -1, +1, piece_type)
        r  = self.check_one_direction(index,  0, +1, piece_type)
        dr = self.check_one_direction(index, +1, +1, piece_type)
        d  = self.check_one_direction(index, +1,  0, piece_type)
        dl = self.check_one_direction(index, +1, -1, piece_type)
        l  = self.check_one_direction(index,  0, -1, piece_type)
        return max([ul + dr + 1, ur + dl + 1, l + r + 1, u + d + 1])
 
    def check_one_direction(self, index, d_row, d_col, piece_type):
        # 0 <= index <= self.num_positions-1
        row, col = self.index2position(index)
        if d_row > 0:
            row_end = self.board_size - 1
        elif d_row < 0:
            row_end = 0
        else:
            row_end = row
 
        if d_col > 0:
            col_end = self.board_size - 1
        elif d_col < 0:
            col_end = 0
        else:
            col_end = col
 
        if d_row == 0:
            limit = int(math.fabs(col_end - col))
        elif d_col == 0:
            limit = int(math.fabs(row_end - row))
        else:
            limit = int(min(math.fabs(row_end-row), math.fabs(col_end-col)))
 
        if piece_type == self.EMPTY_SPOT:
            piece_type = self.board[index]
        for i in xrange(1, limit+1):
            r = row + i * d_row
            c = col + i * d_col
            idx = self.position2index(r, c)
            if self.board[idx] != piece_type:
                return i-1
        return limit

    def game(self):
        print "Welcome to Tic-Tac-Toe. Please make your move selection by " \
          "entering a number corresponding to the movement key on the right."
        b.display_movement()
        b.display_board()

        while True:
            idx = b.get_position()
            print "You have put an X at position %d" % idx
            b.player_move(idx)
            game_over = self.is_game_over(idx, self.PLAYER_PIECE)
            if game_over:
                print "You have beaten my poor AI"
                exit()
            state = b.ai_move(debug=False)
            if state is None:
                print "No more moves, it's a draw"
                exit()
            elif state:
                print "You lose to a computer!"
                exit()
            b.display_movement()
 
 
if __name__ == "__main__":
    b = TicTacToe(board_size=3, win_length=3)
    b.game()
