import copy

class Board():

    def __init__(self, initial_state):
        self.goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,0]]
        self.letter_board = [['a','b','c','d'],['e','f','g','h'],['i','j','k','l']]
        self.state = initial_state
        self.priority = 0
    
    def __str__(self):
        """Returns the current state in string format [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        """
        str_buffer = []

        for row in self.state:
            for tile in row:
                str_buffer.append(str(tile))
        
        out_string = '[{}]'.format(', '.join(str_buffer))

        return out_string
        
    def __lt__(self, other):
        selfPriority = self.priority
        otherPriority = other.priority
        return selfPriority < otherPriority

    def goal_reached(self):
        # Check to see if we have reached the goal state
        return self.state == self.goal_state
    

    def get_moves(self):
        # Returns a list of all valid moves
        valid_moves = []

        # First, find the row and col number of our blank tile (0)
        for row_num, row in enumerate(self.state):
            for col_num, tile in enumerate(row):
                if tile == 0:
                    zero_row = row_num
                    zero_col = col_num
        
        # Check all possible moves. If this move is valid, add its corresponding letter to our valid_moves list
        # Valid-moves list is sorted in descending order (move with last priority will come first in list)
        # 7: UP-LEFT
        next_row = zero_row - 1
        next_col = zero_col - 1
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((7, self.letter_board[next_row][next_col]))

        # 6: LEFT
        next_row = zero_row 
        next_col = zero_col - 1
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((6, self.letter_board[next_row][next_col]))
        
        # 5: DOWN-LEFT
        next_row = zero_row + 1
        next_col = zero_col - 1
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((5, self.letter_board[next_row][next_col]))
        
        # 4: DOWN
        next_row = zero_row + 1
        next_col = zero_col
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((4, self.letter_board[next_row][next_col]))
        
        # 3: DOWN-RIGHT
        next_row = zero_row + 1 
        next_col = zero_col + 1
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((3, self.letter_board[next_row][next_col]))
        
        # 2: RIGHT
        next_row = zero_row 
        next_col = zero_col + 1
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((2, self.letter_board[next_row][next_col]))

        # 1: UP-RIGHT
        next_row = zero_row - 1
        next_col = zero_col + 1
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((1, self.letter_board[next_row][next_col]))

        # 0: UP
        next_row = zero_row - 1
        next_col = zero_col
        if(next_row >= 0 and next_row < 3 and next_col >= 0 and next_col < 4):
            valid_moves.append((0, self.letter_board[next_row][next_col]))

        return valid_moves


    def peek_move(self, next_move_id):
        """Peeks ahead and returns the state of the board if a particular move is taken
        next_move_id should be a char string between 'a' and 'l'
        """

        #temporay board which shows us what the current board would look like if we took the move specified by next_move_id
        temp_board = copy.deepcopy(self.state)

        # First, find row and col number of our blank tile
        for row_num, row in enumerate(self.state):
            for col_num, tile in enumerate(row):
                if tile == 0:
                    zero_row = row_num
                    zero_col = col_num

        # Next, find the row and col numbers of the tile given in the move_id
        for row_num, row in enumerate(self.letter_board):
            for col_num, tile in enumerate(row):
                if tile == next_move_id:
                    next_move_row = row_num
                    next_move_col = col_num

        # Switch our blank tile with the move_id tile
        temp_tile = temp_board[next_move_row][next_move_col]
        temp_board[zero_row][zero_col] = temp_tile
        temp_board[next_move_row][next_move_col] = 0

        return Board(temp_board)


    def get_children(self):
        """Returns all the possible children of a board
        Returns a list of tuples(move, board) where move is a char string between 'a' and 'l' which represents the move, 
        and board is the 2D list representation of the board after the move.
        Return is sorted in descending order (move with last priority will come first in list)
        """

        next_moves = self.get_moves()
        children = []

        for move in next_moves:
            child = self.peek_move(move[1])
            child.priority = move[0]
            children.append((move[1], child))

        return children
        
        