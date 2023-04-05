class StockfishEval:
    def __init__(self, stockfish, input_board, colour):
        # stockfish package stockfish class
        self.fish = stockfish
        # chess package board class
        self.board = input_board
        # fen representation of the board
        self.board_fen = input_board.fen()
        # colour of player with ep opportunity
        self.col = colour
        # last move played (should be a pawn moving 2 ranks)
        self.last_move = str(input_board.peek())
        # resulting row of square that en passant pawn plays into
        self.resulting_row = "6" if self.col == "White" else "3"
        
        # adjacent squares to ep target pawn
        self.squares = {
            "left": "", # return "y" if pawn is on the A file
            "right": "" # return "z" if pawn is on the H file
        }
        
        # if board is on a boundary or not
        self.bounds = {
            "left": False, # True if pawn is on the A file
            "right": False # True if pawn is on the H file
        }
        
        # if there is a valid ep move to play
        self.valid_ep = {
            "left": False, # True if left side can be played
            "right": False # True if right side can be played
        }
        
        # Colour of the playing pawn piece to check
        if self.col == "White":
            self.pawn_piece = self.fish.Piece.WHITE_PAWN
        # if colour is black, we are looking for a black pawn
        else:
            self.pawn_piece = self.fish.Piece.BLACK_PAWN
        
        # list of moves for stockfish to play
        self.move_list = {
            "best_move": "",
            "player_move": "",
            "ep_move_left": "",
            "ep_move_right": ""
        }
    
    '''----------------------------------
    |                                   |
    |        SETTERS AND GETTERS        |
    |                                   |
    ----------------------------------'''
    
    def get_abs_advantage(self, post, pre):
        '''
        Gets the absolute difference of an evaluation
        Need to factor for black side since centipawns is always from White POV
        '''

        difference = post - pre
        if self.col == "White":
            return difference
        else:
            return difference * -1
    
    def get_movelist(self):
        '''Returns the move list'''
        return self.move_list
    
    def set_player_move(self, move):
        '''Sets player move variable in class'''
        self.move_list["player_move"] = move
    
    
    '''----------------------
    |                       |
    |       FUNCTIONS       |
    |                       |
    ----------------------'''
    
    def check_adj_piece(self, square):
        '''Checks if a piece on a square is an opponent pawn'''
        piece = self.fish.get_what_is_on_square(square)
        return True if piece == self.pawn_piece else False
    
    def check_move_is_ep(self, move):
        '''checks if a given move is a valid en-passant move. return bool'''
        move_type = self.fish.will_move_be_a_capture(move)
        ep_type = self.fish.Capture.EN_PASSANT
        if move_type == ep_type:
            return True
        else:
            return False
    
    def find_adj_squares(self):
        '''Returns a tuple of the left and right adjacent squares to a move'''
        
        pawn_move_col = self.last_move[-2] # last move column in the form "a - g"
        pawn_move_row = self.last_move[-1] # last move row in the form "1 - 8"

        # concatenate strings to make a chess square
        self.squares["left"] = self.letter_decrement(pawn_move_col) + pawn_move_row
        self.squares["right"] = self.letter_increment(pawn_move_col) + pawn_move_row
    
    def find_best_move(self):
        '''
        Gets the stockfish evaluation for the best move from a set state
        Returns a tuple of the evaluation, and whether e.p. was the best movee.
        '''

        best_move = self.fish.get_best_move()
        self.move_list["best_move"] = best_move
    
    def find_bounds(self):
        '''Checks if left or right squares are off the board'''
        if self.squares["left"][-2] == "y":
            self.bounds["left"] = True
        if self.squares["right"][-2] == "z":
            self.bounds["right"] = True
    
    def find_ep_moves(self):
        '''Checks if one or two moves are a valid e.p. move. Flag an error
        if neither move is en passant.'''

        # if both left and right can be moved
        if self.valid_ep["left"] and self.valid_ep["right"]:
            # construct a valid en passant move
            move_left = [
                self.letter_decrement(self.last_move[-2]), # file to left of last move
                self.last_move[-1],     # row of last move
                self.last_move[-2],     # file of last move
                self.resulting_row      # row of resulting move
            ]
            # concatentate
            self.move_list["ep_move_left"] = "".join(move_left)
            
            # repeat on right side
            move_right = [
                self.letter_increment(self.last_move[-2]), # file to right of last move
                self.last_move[-1],
                self.last_move[-2],
                self.resulting_row
            ]
            self.move_list["ep_move_right"] = "".join(move_right)
        
        # if en passant can only be played from the right
        if self.valid_ep["right"]:
            # ditto
            move_right = [
                self.letter_increment(self.last_move[-2]), # file to right of last move
                self.last_move[-1],
                self.last_move[-2],
                self.resulting_row
            ]
            self.move_list["ep_move_right"] = "".join(move_right)
        # if en passant can only be played from the left
        elif self.valid_ep["left"]:
            # ditto
            move_left = [
                self.letter_decrement(self.last_move[-2]), # file to left of last move
                self.last_move[-1],
                self.last_move[-2],
                self.resulting_row
            ]
            self.move_list["ep_move_left"] = "".join(move_left)
        # if neither move is en-passant then raise an exception
        else:
            raise Exception('No valid EP moves')
    
    def find_valid_pawns(self):
        '''
        Checks whether the left or right adjacent squares to a pawn
        is a valid en-passant move
        Returns validity of left square, right square as booleans
        '''
        
        # reset the fen of stockfish
        self.reset_fen()
        
        # if somewhere in the middle then check both sides
        if (not self.bounds["left"]) and (not self.bounds["right"]):
            self.valid_ep["left"] = self.check_adj_piece(self.squares["left"])
            self.valid_ep["right"] = self.check_adj_piece(self.squares["right"])
        # if pawn is on A file (leftmost)
        elif self.bounds["left"]:
            # check right only
            self.valid_ep["right"] = self.check_adj_piece(self.squares["right"])
        
        # if pawn is on H file (rightmost)
        elif self.bounds["right"]:
            # check left only
            self.valid_ep["left"] = self.check_adj_piece(self.squares["left"])
    
    def evaluate_board(self):
        '''Evaluates the board at its current state'''
        return self.fish.get_evaluation()
    
    def evaluate_en_passants(self):
        '''Evaluates one or two en-passant moves, and returns the most
        favourable move. '''
        
        # If left and right move can both be played
        if self.valid_ep["left"] and self.valid_ep["right"]:
            # try/except to eliminate an edge case of en-passant moves not being able
            # to be moved from cases such as a pin on the king. if error then evaluate
            # as None (you can't make a super high base case to always trip a case yet
            # since white favours positive evaluations and black favours negative ones)
            try:
                left_eval = self.evaluate_move(self.move_list["ep_move_left"])
            except:
                left_eval = None
            
            try:
                right_eval = self.evaluate_move(self.move_list["ep_move_right"])
            except:
                right_eval = None
            
            # If the colour is white, it favours a larger evaluation
            if self.col == "White":
                # flag up try/except left
                if left_eval == None:
                    return right_eval
                # flag up try/except right
                elif right_eval == None:
                    return left_eval
                # take max if both are valid
                else:                
                    return max(left_eval, right_eval)
            # else => the colour is black, favour a smaller evaluation
            else:
                # same as white side
                if left_eval == None:
                    return right_eval
                elif right_eval == None:
                    return left_eval
                else:
                    return min(left_eval, right_eval)

        # if only right side can be played, return right evaluation
        elif self.valid_ep["right"]:
            return self.evaluate_move(self.move_list["ep_move_right"])
        # if only left side can be played, return left evaluation
        elif self.valid_ep["left"]:
            return self.evaluate_move(self.move_list["ep_move_left"])
    
    def evaluate_move(self, move):
        '''Resets the fen to the board state, and evaluates a given move'''
        self.reset_fen()
        
        # in the form {"type", "value"} where type can be centipawns or mate
        self.fish.make_moves_from_current_position([move])
        return self.evaluate_board()["value"]

    def letter_increment(self, letter):
        '''increments a letter, returns "y" if on the "H" file'''
        if letter == "h":
            return "z"
        return chr(ord(letter) + 1)

    def letter_decrement(self, letter):
        '''decrements a letter, returns "z" if on the "A" file'''
        if letter == "a":
            return "y"
        return chr(ord(letter) - 1)
    
    def reset_fen(self):
        '''resets a fen to its base state'''
        self.fish.set_fen_position(self.board_fen)