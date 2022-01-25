from os import statvfs_result
import numpy as np
from .ai import AI


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((width, height))
        self.turn = 1
        self.end = 1
        self.tie = 0
        self.winner = -1
        self.lastmove_column = -1
        self.lastmove_row = -1

    def print_board(self):
        print(self.board)

    def choose_column(self):
        if self.turn == 1:
            chosencolumn = int(
                input(f"Choose your column [0 : {self.width - 1}]: "))
            while not self.validate_move(chosencolumn):
                chosencolumn = int(
                    input(f"Wrong column! Choose your column [0 : {self.width - 1}]: "))
        else:
            # We should use minimax here
            chosencolumn = self.ai_choose()
        return chosencolumn

    def ai_choose(self):
        # chosencolumn = np.random.randint(0, self.width)
        # while not self.validate_move(chosencolumn):
        #     chosencolumn = np.random.randint(0, self.width)

        agent = AI(self.width, self.height)
        state = (self.board, self.lastmove_row, self.lastmove_column)
        # print("state: ", state)
        # agent.negamax(state, 2, np.inf, np.inf, -1)
        # agent.get_children(state, -1)
        chosencolumn = agent.negamax_decision(state, 5)
        return chosencolumn
        # return 0

    def validate_move(self, column):
        return self.height > column >= 0 and self.board[0][column] == 0

    def drop_piece(self, column):
        last = self.height - 1
        while self.board[last][column] != 0:
            last -= 1
        self.board[last][column] = self.turn
        return last

    def toggle_turn(self):
        self.turn = -self.turn

    def check_tie(self):
        # if there is no more room to drop pieces then self.end = 0 and self.tie = 1
        if 0 not in self.board[0]:
            self.tie = 1
            self.end = 0

    def check_win(self, row, column):
        # if self.turn wins the game then self.end = 0 and self.winner = self.turn
        counter = 1
        # check RIGHT of dropped piece
        for j in range(column, self.width - 1):
            if self.board[row][j + 1] != self.turn:
                break
            counter = counter + 1
        # check LEFT of dropped piece
        for j in range(column, 0, -1):
            if self.board[row][j - 1] != self.turn:
                break
            counter = counter + 1
        if counter == 4:
            self.end = 0
            self.winner = self.turn
            return
        counter = 1
        # check DOWN of dropped piece
        for i in range(row, self.height - 1):
            if self.board[i + 1][column] != self.turn:
                break
            counter = counter + 1
        # check up vertical
        for i in range(row, 0, -1):
            if self.board[i - 1][column] != self.turn:
                break
            counter = counter + 1
        if counter == 4:
            self.end = 0
            self.winner = self.turn
            return
        counter = 1
        # check UP/LEFT of dropped piece
        for i, j in zip(range(row, 0, -1), range(column, 0, -1)):
            if self.board[i - 1][j - 1] != self.turn:
                break
            counter = counter + 1
        # check DOWN/RIGHT of dropped piece
        for i, j in zip(range(row, self.height - 1), range(column, self.width - 1)):
            if self.board[i + 1][j + 1] != self.turn:
                break
            counter = counter + 1
        if counter == 4:
            self.end = 0
            self.winner = self.turn
            return
        counter = 1
        # check UP/RIGHT of dropped piece
        for i, j in zip(range(row, 0, -1), range(column, self.width - 1)):
            if self.board[i - 1][j + 1] != self.turn:
                break
            counter = counter + 1
        # check DOWN/LEFT of dropped piece
        for i, j in zip(range(row, self.height - 1), range(column, 0, -1)):
            if self.board[i + 1][j - 1] != self.turn:
                break
            counter = counter + 1
        if counter == 4:
            self.end = 0
            self.winner = self.turn
            return

    def start_game(self):
        while self.end:
            chosencolumn = self.choose_column()
            chosenrow = self.drop_piece(chosencolumn)
            self.print_board()
            self.check_win(chosenrow, chosencolumn)
            self.check_tie()
            self.toggle_turn()
            self.lastmove_row, self.lastmove_column = chosenrow, chosencolumn
        if self.tie == 1:
            print("tie")
        else:
            print(f"{self.winner} wins the game")
