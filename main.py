import random
from src.data.prepare_data import load_split
from src.game.game import nytConnections
from src.simple_solvers.random_solver import random_solver

# This function plays every puzzle with the given solver
def evaluate(solver, puzzles):
    wins = 0
    solved = 0

    for p in puzzles:
        game = nytConnections([g["members"] for g in p["groups"]])
        wins += solver(game)
        solved += game.MAX_CONNECTIONS - game.remaining_connections
    # return number of wins and avg number of groups solved per puzzle
    return wins, solved / len(puzzles)

if __name__ == "__main__":
    # ensure every run gets the same random seed so results are repeatable
    # CHANGE LATER FOR BETTER REPORT RESULTS?
    # random.seed(0)
    tune = load_split("tune")
    wins, avg = evaluate(random_solver, tune)
    print(f"Random: {wins}/{len(tune)} wins, {avg:.2f} groups solved on average")

