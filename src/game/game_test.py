"""
The following is a hardcoded test set we can use to test our progress:
"""

from game import nytConnections

groups = [
    ["SNOW", "ICE", "FROST", "COLD"],
    ["FIRE", "FLAME", "HEAT", "BURN"],
    ["CAT", "DOG", "MOUSE", "HAMSTER"],
    ["RED", "BLUE", "GREEN", "YELLOW"]
]

g = nytConnections(groups)

print(f"Current board, before any guesses: {g.return_current_board()}")
# GUESSES MUST BE IN CAPS
print(g.guess(["SNOW", "ICE", "FROST", "COLD"]))   # correct
print(g.guess(["FIRE", "FLAME", "HEAT", "CAT"]))    # one away
print(g.guess(["FIRE", "FLAME", "HEAT", "CAT"]))     # invalid (repeat)
print(g.guess(["SNOW", "FIRE", "FLAME", "HEAT"]))   # invalid (already solved)
print(g.guess(["FIRE", "CAT", "RED", "DOG"]))       # incorrect
print(g.mistakes_left)  

print(f"Is the game over? {g.is_over()} ")
print(f"Did you win? {g.is_won()} ")
print(f"Return current board: {g.return_current_board()}")