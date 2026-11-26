import random

def random_solver(game):
    while not game.is_over():
        guess = random.sample(game.return_current_board(), 4)
        if set(guess) in game.past_guesses:
            continue
        game.guess(guess)
    return game.is_won()