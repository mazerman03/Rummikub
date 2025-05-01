from source.player import Player
from source.board import Board
from source.tile import Tile
import pygame

import random

class Game:
    def __init__(self, player_names=None):

        #TODO: Placeholder for player logic, need to update to work with custom names and numbers up to 6
        if player_names is None:
            player_names = ["Noe", "Max"]

        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0
        self.board = Board()
        self.tile_bag = self.create_tile_bag()
        self.deal_initial_tiles()

    #TODO: Haven't introduced jokers into the mix, might be easier to do without them then include them at the end. 
    def create_tile_bag(self):
        """Create a list of all the tiles in the game."""
        colors = ['blue', 'red', 'yellow', 'black']
        tiles = [Tile(color, number) for color in colors for number in range(1, 14)]
        tiles *= 2  # Duplicate tiles, since there are 2 of each color-number combination
        random.shuffle(tiles)
        return tiles

    def deal_initial_tiles(self):
        for player in self.players:
            for _ in range(14):
                if self.tile_bag:
                    tile = self.tile_bag.pop()
                    player.draw_tile(tile)


    def play_turn(self):
        player = self.players[self.current_player_index]
        print(f"\n{player.name}'s turn. Hand: {player.hand}")

        # Placeholder for actual play logic
        if not self.try_to_play(player):
            self.draw_tile(player)

        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def draw_tile(self, player):
        """Draw a tile from the bag and add it to the player's hand."""
        if self.tile_bag:
            tile = self.tile_bag.pop()
            player.draw_tile(tile)
            print(f"{player.name} drew a tile: {tile}")
        else:
            print("No more tiles to draw!")


    #TODO: Hardest part actually, to create the game logic, ill think about it next week
    def try_to_play(self, player):
        
        print(f"{player.name} has no valid plays (simulated).")
        return False

    def next_turn(self):
        """Switch to the next player's turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        print(f"Now it's {self.players[self.current_player_index].name}'s turn!")

    def game_over(self):
        """Check if the game is over (any player has no tiles)."""
        return any(not player.has_tiles() for player in self.players)


    #TODO: Hard part as well now its not really doing anything but simulate turns 
    def play_turn(self):
        """Simulate the game logic for the current turn."""
        player = self.players[self.current_player_index]
        print(f"\n{player.name}'s turn. Hand: {player.hand}")

        # TODO: If the player has no tiles, theyve won the game round, message displaying the winner needed
        # if not player.has_tiles():
        #     #self.player.won()


        #TODO: Implement a valid move checker for a player,  
        if player.can_play():
            # Placeholder: Add logic to make a move, e.g., form a set/run
            print(f"{player.name} is playing a tile.")
            self.board.add_set_or_run([player.play_tile(player.hand[0])])  # Just an example of a tile being played

        # After the turn, switch to the next player
        self.next_turn()

#Pygame settings 

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rummikub Game")
timer = pygame.time.Clock()
font = pygame.font.Font(None, 36)



run = True
while run:
    timer.tick(FPS)
    screen.fill('grey')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.flip()
