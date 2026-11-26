class nytConnections:
    MAX_CONNECTIONS = 4
    MAX_MISTAKES = 4

    def __init__(self, groups):
        # Initalize a set for each group passed in as a list. We chose to use a set since
        # order does not matter when comparing sets, important for when the user submits an answer
        self.groups = [set(g) for g in groups]
        # Add all available words into a single set:
        self.remaining = set()
        for group in groups:
            for word in group:
                self.remaining.add(word)
        # Store solved groups in here:
        self.connections = []
        # Groups that still need to be solved
        self.remaining_connections = self.MAX_CONNECTIONS
        self.mistakes_left = self.MAX_MISTAKES
        # Keep a record of all past guesses as well to ensure repeat guesses are not accepted
        self.past_guesses = []

    def guess(self, words):
        user_guess = set(words)
        if (len(user_guess) != 4) or not (user_guess <= self.remaining) or (user_guess in self.past_guesses):
            # EXPAND ON THIS LATER (MORE ERRORS?)
            return "Invalid Guess"
        self.past_guesses.append(user_guess)

        for group in self.groups:
            if (user_guess == group):
                self.connections.append(user_guess)
                self.remaining -= group
                self.remaining_connections -= 1
                return "Correct"

        self.mistakes_left -= 1

        for group in self.groups:
            if len(user_guess & group) == 3:
                return "One Away!"
        return "Incorrect"

    def is_won(self):
        return self.remaining_connections == 0

    def is_over(self):
        return self.is_won() or self.mistakes_left == 0

    def return_current_board(self):
        # Return the current board and what words remain. This is sorted
        # so that our random solver is able to have consistent inputs
        return sorted(self.remaining)