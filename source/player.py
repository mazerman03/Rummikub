class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []  # List of tiles in hand
        self.played_tiles = []  # Tiles that have been played to the board

    def draw_tile(self, tile):
        """Draw a tile into the player's hand."""
        self.hand.append(tile)

    def has_tiles(self):
        """Check if the player has any tiles left."""
        return len(self.hand) > 0

    #TODO: This where the adding to tiles to sets and other logic happens.
    #TODO2: implement the first turn logic to the game. 
    def play_tile(self, tile):
        """Play a tile from the player's hand to the board."""
        if tile in self.hand:
            self.hand.remove(tile)
            return tile
        return None

    #TODO: This needs to be further developed to check for valid plays when given a board state. 
    def can_play(self):
        """Check if the player can play any tile (placeholder for your logic)."""
        return self.has_tiles()

    def __repr__(self):
        return f"Player {self.name}: {self.hand}"
