import numpy as np

class AI:
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width
    
    def negamax(self, state, depth, alpha, beta, color):
        if self.is_terminal(state) or depth <= 0:
            # val =  color * self.eval_function(state)
            # return val
            return 0

        value = -np.inf
        children = self.get_children(state, color)
        # children = sorted(children, key=lambda x: self.eval_function(x))

        for child in children:

            value = max(value, -self.negamax(child, depth-1, -beta, -alpha, -color))
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break

        return value

    def is_terminal(self, state):
        pass

    def eval_function(self, state):
        pass

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
        print(len(children))
        return children

    def drop_piece(self, board, turn, column):
            last = self.height - 1
            while board[last][column] != 0:
                last -= 1
            board[last][column] = turn
            return last
    
    def validate_move(self, board, column):
        return self.height > column >= 0 and board[0][column] == 0