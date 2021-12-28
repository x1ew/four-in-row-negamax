import numpy as np


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((width, height))
        self.player = 1
        self.AI = 2
        self.turn = 1
        self.end = 1
        self.tie = 0
        self.winner = -1

    def print_board(self):
        print(self.board)

    def choose_column(self):
        if self.turn == 1:
            chosencolumn = int(input(f"Choose your column [0 : {self.width - 1}]: "))
            while not self.validate_move(chosencolumn):
                chosencolumn = int(input(f"Wrong column! Choose your column [0 : {self.width - 1}]: "))
        else:
            # We should use minimax here
            chosencolumn = self.ai_choose()
        return chosencolumn

    def ai_choose(self):
        return np.random.randint(0, self.width)

    def validate_move(self, column):
        return self.height > column >= 0 and self.board[0][column] == 0

    def drop_piece(self, column):
        last = self.height - 1
        while self.board[last][column] != 0:
            last -= 1
        self.board[last][column] = self.turn

    def toggle_turn(self):
        self.turn = 1 if self.turn == 2 else 2

    def check_tie(self):
        # if there is no more room to drop pieces then self.end = 0 and self.tie = 1
        pass

    def check_win(self):
        # if self.turn wins the game then self.end = 0 and self.winner = self.turn
        pass

    def start_game(self):
        while self.end:
            chosencolumn = self.choose_column()
            self.drop_piece(chosencolumn)
            self.print_board()
            if self.check_win() or self.check_tie():
                break
            self.toggle_turn()
        if self.tie == 1:
            print("tie")
        else:
            print(f"{self.winner} wins the game")
