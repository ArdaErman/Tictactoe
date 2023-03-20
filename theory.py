import math
import random


class Player():
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

        # we want all players to get their next move
        def get_move(self, game):
            pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random valid spot for our next move
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            # we're going to check that this is a correct value by trying to cast
            # it to an integer, and if it is not, then we say it's invalid.
            # if that spot is not available on the board, we also say it's invalid.
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True  # if these are successful, then yay!
            except ValueError:
                print('Invalid square. Please try again.')

        return val


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9 and self.letter == 'X':
            # Choose one of the best moves for the first move of the game
            best_moves = [0, 2, 6, 8]
            square = random.choice(best_moves)
        else:
            # Use the minimax algorithm to choose the best move
            if len(game.available_moves()) == 9:
                square = random.choice(game.available_moves())
            else:
                square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself!
        # the other player... so whatever the letter is not
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move was a winner
        # this is our base case
        if state.current_winner == other_player:
            # we should return position AND score because we need to keep track of the score
            # for minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)
                    }

        elif not state.empty_squares():  # no empty squares
            return {'position': None, 'score': 0}

        if player == max_player:
            # each score should maximize (be larger)
            best = {'position': None, 'score': -math.inf}
        else:
            # each score should minimize
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)
            # step 2: recurse using minimax to simulate a game after making that move
            # now we alternate players
            sim_score = self.minimax(state, other_player)

            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            # otherwise this will get messed up from the recursion
            sim_score['position'] = possible_move

            # step 4: update the dictionaries if necessary
            if player == max_player:  # we are trying to maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score  # replace best
            else:  # but minimise the other player
                if sim_score['score'] < best['score']:
                    best = sim_score  # replace best

        return best
