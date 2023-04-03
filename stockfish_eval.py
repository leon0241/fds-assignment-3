class StockfishEval:
    def __init__(self, stockfish, input_board, colour):
        self.fish = stockfish
        self.board = input_board
        self.board_fen = input_board.fen()
        self.col = colour
        self.last_move = str(input_board.peek())
        self.resulting_row = "6" if self.col == "White" else "3"
        
        self.squares = {
            "left": "",
            "right": ""
        }
        
        self.bounds = {
            "left": False,
            "right": False
        }
        
        self.valid_ep = {
            "left": False,
            "right": False
        }
        
        if self.col == "White":
            self.pawn_piece = self.fish.Piece.WHITE_PAWN
        # if colour is black, we are looking for a black pawn
        else:
            self.pawn_piece = self.fish.Piece.BLACK_PAWN
        
        self.move_list = {
            "best_move": "",
            "player_move": "",
            "ep_move_left": "",
            "ep_move_right": ""
        }
    
    def set_player_move(self, move):
        self.move_list["player_move"] = move
    
    def get_movelist(self):
        return self.move_list
    
    def evaluate_board(self):
        return self.fish.get_evaluation()
    
    def evaluate_move(self, move):
        self.reset_fen()
        self.fish.make_moves_from_current_position([move])
        
        raw_value = self.evaluate_board()["value"]
        return raw_value
    
    def evaluate_en_passants(self):
        if self.valid_ep["left"] and self.valid_ep["right"]:
            try:
                left_eval = self.evaluate_move(self.move_list["ep_move_left"])
            except:
                left_eval = None
            
            try:
                right_eval = self.evaluate_move(self.move_list["ep_move_right"])
            except:
                right_eval = None
            
            if self.col == "White":
                if left_eval == None:
                    left_eval = -10000
                elif right_eval == None:
                    right_eval = -10000
                return max(left_eval, right_eval)
            else:
                if left_eval == None:
                    left_eval = 10000
                elif right_eval == None:
                    right_eval = 10000
                return min(left_eval, right_eval)
            
        elif self.valid_ep["right"]:
            return self.evaluate_move(self.move_list["ep_move_right"])
        elif self.valid_ep["left"]:
            return self.evaluate_move(self.move_list["ep_move_left"])
        
    def evaluate_best_move(self):
        return self.evaluate_move(self.move_list["best_move"])
    
    def evaluate_player_move(self):
        return self.evaluate_move(self.move_list["player_move"])
        
    def check_move_is_ep(self, move):
        # print(self.fish.get_board_visual())
        # print(move)
        move_type = self.fish.will_move_be_a_capture(move)
        ep_type = self.fish.Capture.EN_PASSANT
        if move_type == ep_type:
            return True
        else:
            return False
    
    def increment_letter(self, letter):
        '''increments a letter, returns "y" if on the "H" file'''
        if letter == "h":
            return "z"
        return chr(ord(letter) + 1)

    def decrement_letter(self, letter):
        '''decrements a letter, returns "z" if on the "A" file'''
        if letter == "a":
            return "y"
        return chr(ord(letter) - 1)
    
    def reset_fen(self):
        self.fish.set_fen_position(self.board_fen)
    
    def check_adj_piece(self, square):
        '''Checks if a piece on a square is an opponent pawn'''
        print(square)
        piece = self.fish.get_what_is_on_square(square)
        print(piece)
        print(self.pawn_piece)
        print(piece == self.pawn_piece)
        return True if piece == self.pawn_piece else False
    
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
    
    def get_best_move(self):
        '''
        Gets the stockfish evaluation for the best move from a set state
        Returns a tuple of the evaluation, and whether e.p. was the best movee.
        '''

        best_move = self.fish.get_best_move()
        
        self.move_list["best_move"] = best_move
        
        # # if the best move is en-passant
        # ep_best = False
        # if self.fish.will_move_be_a_capture(best_move) == self.fish.Capture.EN_PASSANT:
        #     ep_best = True
        
        # # play best move and measure evaluation
        # self.fish.make_moves_from_current_position([best_move])
        # post_eval = self.fish.get_evaluation()
        
        # # get difference of best move against the previous evaluation
        # post_eval_best_diff = get_abs_advantage(post_eval["value"], pre_eval["value"], col)

        # return [post_eval_best_diff, ep_best]
           
    def find_adj_squares(self):
        '''
        Returns a tuple of the left and right adjacent squares to a move
        '''
        # resulting column in the form "a - g"
        pawn_move_col = self.last_move[-2]
        # resulting row in the form "1 - 8"
        pawn_move_row = self.last_move[-1]

        # concatenate strings to make a square
        self.squares["left"] = self.decrement_letter(pawn_move_col) + pawn_move_row
        self.squares["right"] = self.increment_letter(pawn_move_col) + pawn_move_row
    
    def find_bounds(self):
        if self.squares["left"][-2] == "y":
            self.bounds["left"] = True
        if self.squares["right"][-2] == "z":
            self.bounds["right"] = True
    
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
            print(self.valid_ep)
        # if pawn is on A file (leftmost)
        elif self.bounds["left"]:
            # check right only
            self.valid_ep["right"] = self.check_adj_piece(self.squares["right"])
        
        # if pawn is on H file (rightmost)
        elif self.bounds["right"]:
            # check left only
            self.valid_ep["left"] = self.check_adj_piece(self.squares["left"])
        print(self.fish.get_board_visual())
        print(self.bounds)
        print(self.squares)
        print(self.valid_ep)
    
    def find_ep_moves(self):
        if self.valid_ep["left"] and self.valid_ep["right"]:
            # concat a valid en passant move
            move_left = [
                self.decrement_letter(self.last_move[-2]),
                self.last_move[-1],
                self.last_move[-2],
                self.resulting_row
            ]
            self.move_list["ep_move_left"] = "".join(move_left)
            
            move_right = [
                self.increment_letter(self.last_move[-2]),
                self.last_move[-1],
                self.last_move[-2],
                self.resulting_row
            ]
            self.move_list["ep_move_right"] = "".join(move_right)
        
        # if en passant can only be played from the right
        if self.valid_ep["right"]:
            move_right = [
                self.increment_letter(self.last_move[-2]),
                self.last_move[-1],
                self.last_move[-2],
                self.resulting_row
            ]
            self.move_list["ep_move_right"] = "".join(move_right)
        # if en passant can only be played from the left
        elif self.valid_ep["left"]:
            move_left = [
                self.decrement_letter(self.last_move[-2]),
                self.last_move[-1],
                self.last_move[-2],
                self.resulting_row
            ]
            self.move_list["ep_move_left"] = "".join(move_left)
        else:
            raise Exception('No valid EP moves')