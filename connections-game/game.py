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

