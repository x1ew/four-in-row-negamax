import numpy as np

class AI:
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width
    
    def negamax(self, state, depth, alpha, beta, color):
        if self.is_terminal(state) or depth <= 0:
            val =  color * self.eval_function(state)
            return val

        value = -np.inf
        children = self.get_children(state, color)
        children = sorted(children, key=lambda x: self.eval_function(x))

        for child in children:

            value = max(value, -self.negamax(child, depth-1, -beta, -alpha, -color))
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break

        return value

    def is_terminal(self, state):
        board, _, _ = state
        if 0 not in board[0]:
            return True
        return np.isinf(np.abs(self.eval_function(state)))

    def eval_function(self, state):
        board, row, column = state
        hval = 0
        color = board[row][column]

        counter = 1
        # check RIGHT of dropped piece
        for j in range(column, self.width - 1):
            if board[row][j + 1] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        for j in range(column, 0, -1):
            if board[row][j - 1] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        
        if counter == 4:
            return color * np.inf     
        if counter == 3:
            hval += 900000
        if counter == 2:
            hval += 4000
        
        counter = 1
        for i in range(row, self.height - 1):
            if board[i + 1][column] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf

        for i in range(row, 0, -1):
            if board[i - 1][column] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        
        if counter == 4:
            return color * np.inf     
        if counter == 3:
            hval += 900000
        if counter == 2:
            hval += 4000

        for i, j in zip(range(row, 0, -1), range(column, 0, -1)):
            if board[i - 1][j - 1] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        for i, j in zip(range(row, self.height - 1), range(column, self.width - 1)):
            if board[i + 1][j + 1] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        
        if counter == 4:
            return color * np.inf     
        if counter == 3:
            hval += 900000
        if counter == 2:
            hval += 4000
        
        counter = 1
        for i, j in zip(range(row, 0, -1), range(column, self.width - 1)):
            if board[i - 1][j + 1] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        for i, j in zip(range(row, self.height - 1), range(column, 0, -1)):
            if board[i + 1][j - 1] != color:
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf

        if counter == 4:
            return color * np.inf     
        if counter == 3:
            hval += 900000
        if counter == 2:
            hval += 4000
        
        return color * hval

    def get_children(self, state, color):
        board, i, j  = state
        # color = board[i][j]
        children = []

        for c in range(self.width):
            if self.validate_move(board, c):
                
                child_board = board.copy()
                
                r = self.drop_piece(child_board, color, c)

                child_state = (child_board, c, r)
                children.append(child_state)
        # print(len(children))
        return children

    def drop_piece(self, board, turn, column):
            last = self.height - 1
            while board[last][column] != 0:
                last -= 1
            board[last][column] = turn
            return last
    
    def validate_move(self, board, column):
        return self.height > column >= 0 and board[0][column] == 0

    def negamax_decision(self, state, depth):
        children = self.get_children(state, -1)    
        # random.shuffle(children)
    
        child_board, decision, decision_row = children[0]    
        value = -np.inf
        for child in children:
            new_value = -self.negamax(child, depth-1, -np.inf, np.inf, -1)
            if new_value > value:
                decision = child[1]
                value = new_value         
    
        return decision