import sys
import time
import getopt

import random


class Tic(object):
    winning_combos = (
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('-1', '0', '1')

    squares = []

    #def __init__(self, squares=[]):
    #    if len(squares) == 0:
    #        self.squares = ['_' for i in range(9)]
    #    else:
    #        self.squares = squares

    def show(self):
        #for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
        #    print element
        board = ''.join(self.squares)
        if len(board) == 9:
            print("           ")
            for line in range(3):
                line_str = ''
                line_bar = ['','|','|']
                for item in board[line*3:line*3+3]:
                    if item.upper() == 'X':
                        line_str += ' X ' + line_bar.pop()
                    elif item.upper() == 'O':
                        line_str += ' O ' + line_bar.pop()
                    else:
                        line_str += '   ' + line_bar.pop()
                print(line_str)
                if line == 2:
                    print("           ")
                else:
                    print("-----------")

    def available_moves(self):
        """what spots are left empty?"""
        return [k for k, v in enumerate(self.squares) if v is '_']

    def available_combos(self, player):
        """what combos are available?"""
        return self.available_moves() + self.get_squares(player)

    def complete(self):
        """is the game over?"""
        if '_' not in [v for v in self.squares]:
            return True
        if self.winner() != '_':
            return True
        return False

    def X_won(self):
        return self.winner() == 'X'

    def O_won(self):
        return self.winner() == 'O'

    def tied(self):
        return self.complete() == True and self.winner() is '_'

    def winner(self):
        for player in ('X', 'O'):
            positions = self.get_squares(player)
            for combo in self.winning_combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player
        return '_'

    def get_squares(self, player):
        """squares that belong to a player"""
        return [k for k, v in enumerate(self.squares) if v == player]

    def make_move(self, position, player):
        """place on square on the board"""
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            if node.X_won():
                return -1
            elif node.tied():
                return 0
            elif node.O_won():
                return 1
        for move in node.available_moves():
            node.make_move(move, player)
            val = self.alphabeta(node, get_enemy(player), alpha, beta)
            node.make_move(move, '_')
            if player == 'O':
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta


def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        val = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, '_')
        print("move:", move + 1, "causes:", board.winners[val + 1])
        if val > a:
            a = val
            choices = [move]
        elif val == a:
            choices.append(move)
    return random.choice(choices)


def get_enemy(player):
    if player == 'X':
        return 'O'
    return 'X'

if __name__ == "__main__":
    argv = sys.argv[1:]
    board = Tic()
    try:
        opts, args = getopt.getopt(argv,"hf:b:v",["first=","board=","verbose="])
        for opt, arg in opts:
            if opt == '-h':
                print("%s -f x -b ____x____"%(__file__))
                sys.exit()
            elif opt in ("-v", "--verbose"):
                board.show()
            elif opt in ("-b", "--board"):
                if len(arg) == 9:
                    board.squares = list(arg)
                else:
                    print("wrong board!")
            elif opt in ("-f", "--first"):
                player = args
        player_move = board.squares.index('x')
        if not player_move in board.available_moves():
            board.complete()
        board.make_move(player_move, player)
        computer_move = determine(board, player)

    except getopt.GetoptError:
        print("%s -f x -b ____x____"%(__file__))
        sys.exit(2)