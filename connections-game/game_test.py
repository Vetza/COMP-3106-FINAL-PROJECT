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

print(g.guess(["snow", "ice", "frost", "cold"]))   # correct
print(g.guess(["fire", "flame", "heat", "cat"]))    # one_away
print(g.guess(["fire", "flame", "heat", "cat"]))     # invalid (repeat)
print(g.guess(["snow", "fire", "flame", "heat"]))   # invalid (snow already solved)
print(g.guess(["fire", "cat", "red", "dog"]))       # incorrect
print(g.mistakes_left)  