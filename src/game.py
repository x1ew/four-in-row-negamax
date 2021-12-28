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

    def print_board(self):
        print(self.board)

    def choose_row(self):
        chosenrow = -1
        if self.turn == 1:
            chosenrow = int(input("Choose your row: "))
            while not self.validate_move(chosenrow):
                chosenrow = int(input("Wrong row! Choose your row: "))
        else:
            # We should use minimax here
            chosenrow = self.AI_choose()
        return chosenrow

    def ai_choose(self):
        return np.random.randint(1, self.width)

    def validate_move(self, row):
        return self.height > row > 1 and self.board[0][row] == 0

    def drop_piece(self, row):
        last = self.height - 1
        while self.board[last][row] != 0:
            last -= 1
        self.board[last][row] = self.turn

    def toggle_turn(self):
        self.turn = 1 if self.turn == 2 else 2

    def start_game(self):
        while self.end:
            chosenrow = self.choose_row()
            self.drop_piece(chosenrow)
            self.print_board()
            self.toggle_turn()
