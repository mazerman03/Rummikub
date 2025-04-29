class Board:
    def __init__(self):
        self.sets_and_runs = []  # List to hold sets and runs

    #TODO: this is a board wide check that needs to be implemented
    def add_set_or_run(self, group):
        """Add a set or run to the board."""
        self.sets_and_runs.append(group)

    #TODO: We can either validate moves via player check or board check, might need to use both to be safe but we'll see with processing resources. 
    def can_add_group(self, group):
        """Check if a set or run is valid (placeholder for logic)."""
        return True

    #Should not display any until logic to add sets and runs to the board is implemented
    def display(self):
        """Display the current state of the board."""
        print("Current Board:")
        for group in self.sets_and_runs:
            print(group)

    def __repr__(self):
        return f"Board: {self.display()}"
