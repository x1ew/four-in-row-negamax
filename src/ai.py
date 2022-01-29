import numpy as np
import random


class AI:
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width

    def negamax(self, state, depth, alpha, beta, color):
        #last move + last depth
        if self.is_terminal(state, -color) or depth <= 0:
            val = color * \
                self.eval_function(state, -color) * (1 + 0.001 * depth)
            return val

        value = -np.inf
        children = self.get_children(state, color)
        random.shuffle(children) #for same values
        children = sorted(
            children, key=lambda x: self.eval_function(x, -color))

        for child in children:
            new_value = -self.negamax(child, depth-1, -beta, -alpha, -color)
            # print("+-----------------+")
            # print(child)
            # print(new_value)
            # print("+-----------------+")
            value = max(value, new_value)
            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value

    def is_terminal(self, state, color):
        board, _, _ = state
        if 0 not in board[0]:
            return True
        return np.isinf(np.abs(self.eval_function(state, color))) #check for inf

    def eval_function(self, state, color):
        board, row, column = state
        #startvalue -> 0
        hval = 0
        # ccolor = board[row][column]
        # print("eval: inp is", color, "last is", ccolor)

        counter = 1
        point = 0 #if there are 3, and next to them is free -> get more point
        
        # check RIGHT of dropped piece
        for j in range(column, self.width - 1):
            if board[row][j + 1] != color:
                if board[row][j + 1] == 0: 
                    point += 1
                break 
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        
        # check LEFT of dropped piece
        for j in range(column, 0, -1):
            if board[row][j - 1] != color:
                if board[row][j - 1] == 0:
                    point += 1
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf

        if counter == 4:
            return color * np.inf
        if counter == 3:
            if point == 2:
                hval += 900000
            elif point == 1:
                hval += 50000
        if counter == 2:
            if point == 2:
                hval += 4000
            elif point == 1:
                hval += 3000
        # print("right left ", hval)

        # check DOWN of dropped piece
        counter = 1
        point = 0
        for i in range(row, self.height - 1):
            if board[i + 1][column] != color:
                if board[i + 1][column] == 0:
                    point += 1
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf

        # check UP of dropped piece
        for i in range(row, 0, -1):
            if board[i - 1][column] != color:
                if board[i - 1][column] == 0:
                    point += 1
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf

        if counter == 4:
            return color * np.inf
        if counter == 3:
            if point == 2:
                hval += 900000
            elif point == 1:
                hval += 50000
        if counter == 2:
            if point == 2:
                hval += 4000
            elif point == 1:
                hval += 3000
        # print("top down ", hval)

        # check UP/LEFT of dropped piece
        counter = 1
        point = 0
        for i, j in zip(range(row, 0, -1), range(column, 0, -1)):
            if board[i - 1][j - 1] != color:
                if board[i - 1][j - 1] == 0:
                    point += 1
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        
        # check DOWN/RIGHT of dropped piece
        for i, j in zip(range(row, self.height - 1), range(column, self.width - 1)):
            if board[i + 1][j + 1] != color:
                if board[i + 1][j + 1] == 0:
                    point += 1
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf

        if counter == 4:
            return color * np.inf
        if counter == 3:
            if point == 2:
                hval += 900000
            elif point == 1:
                hval += 50000
        if counter == 2:
            if point == 2:
                hval += 4000
            elif point == 1:
                hval += 3000
        # print("topleft botright ", hval)

        # check UP/RIGHT of dropped piece
        counter = 1
        point = 0
        for i, j in zip(range(row, 0, -1), range(column, self.width - 1)):
            if board[i - 1][j + 1] != color:
                if board[i - 1][j + 1] == 0:
                    point += 1
                break
            counter = counter + 1
            if counter == 4:
                return color * np.inf
        
        # check DOWN/LEFT of dropped piece
        for i, j in zip(range(row, self.height - 1), range(column, 0, -1)):
            if board[i + 1][j - 1] != color:
                if board[i + 1][j - 1] == 0:
                    point += 1
                break
            counter = counter + 1
            if counter == 4: 
                return color * np.inf

        if counter == 4:
            return color * np.inf
        if counter == 3:
            if point == 2:
                hval += 900000
            elif point == 1:
                hval += 50000
        if counter == 2:
            if point == 2:
                hval += 4000
            elif point == 1:
                hval += 3000
        # print("topright botleft ", hval)
        return color * hval

    def get_children(self, state, color):
        board, i, j = state
        # color = board[i][j]
        # color = -color
        children = []

        #drop in every columns
        for c in range(self.width):
            if self.validate_move(board, c):

                child_board = board.copy()

                r = self.drop_piece(child_board, color, c)

                child_state = (child_board, r, c)
                children.append(child_state)
        # print(len(children))
        return children

    def drop_piece(self, board, turn, column):
        #check for where to drop
        last = self.height - 1
        while board[last][column] != 0:
            last -= 1
        board[last][column] = turn
        return last

    def validate_move(self, board, column):
        #check for empty column for droping (0 & empty)
        return self.height > column >= 0 and board[0][column] == 0

    def negamax_decision(self, state, depth):
        color = -1
        children = self.get_children(state, color)
        random.shuffle(children) #for choosing children with equal state
        child_board, decision_row, decision_column = children[0] #choose first one for comparing
        value = -np.inf

        for child in children:
            new_value = -self.negamax(child, depth-1, -np.inf, np.inf, -color)
            print("+----------------+----------------+")
            print(child)
            print(new_value)
            print("+----------------+----------------+")
            if new_value > value:
                print(value, "changed to", new_value)
                decision_column = child[2]
                value = new_value
        return decision_column
