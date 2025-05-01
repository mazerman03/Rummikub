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


game = Game(player_names=["Jugador 1", "Jugador 2"])

selected_tile = None

#Pygame settings 

pygame.init()
pygame.font.init()

# Define the colors
BLACK = (0, 0, 0)
DARKGREY = (99, 99, 99)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
 
# Define the dimensions of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
# Define the dimensions of the tiles
TILE_WIDTH = 50
TILE_HEIGHT = 70
 
# Define the number of tiles in the pool
POOL_SIZE = 106
 
# Define the number of tiles in a rack
RACK_SIZE = 14
 
# Define the number of tiles in a group
GROUP_SIZE = 3
 
# Define the number of colors
NUM_COLORS = 5
 
# Define the number of runs
NUM_RUNS = 2
 
# Define the number of tiles per run
TILES_PER_RUN = 4
 
# Define the number of tiles per group
TILES_PER_GROUP = 5
 
# Define the number of tiles per player
TILES_PER_PLAYER = 13
 
# Define the number of players
NUM_PLAYERS = 3
 
# Define the font size
FONT_SIZE = 20
 
# Define the font
FONT = pygame.font.Font(None, FONT_SIZE)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window title
pygame.display.set_caption("Rummykub Game")

def get_color_from_tile(tile):
    color_map = {
        'red': RED,
        'blue': BLUE,
        'yellow': (255, 255, 0),
        'black': BLACK
    }
    return color_map.get(tile.color, WHITE)

def draw_tiles():
    screen.fill(DARKGREY)
    
    # Draw the pool (using game.tile_bag)
    for i in range(5):
        pygame.draw.rect(screen, WHITE, (10, 10 + i*80, TILE_WIDTH, TILE_HEIGHT))
    
    # Draw the hand of each player (racks)
    for i, player in enumerate(game.players):
        for j, tile in enumerate(player.hand):
            color = get_color_from_tile(tile) 
            x = 100 + j * TILE_WIDTH
            y = 10 + i * 80
            pygame.draw.rect(screen, color, (x, y, TILE_WIDTH, TILE_HEIGHT))
            # Draw the tile number
            text = FONT.render(str(tile.number), True, BLACK)
            text_rect = text.get_rect(center=(x + TILE_WIDTH//2, y + TILE_HEIGHT//2))
            screen.blit(text, text_rect)
    
    # Draw the board (sets and runs)
    for i, group in enumerate(game.board.sets_and_runs): 
        for j, tile in enumerate(group):
            x = 10 + j * TILE_WIDTH
            y = 410 + i * 80
            pygame.draw.rect(screen, get_color_from_tile(tile), (x, y, TILE_WIDTH, TILE_HEIGHT))
    
    pygame.display.flip()

def handle_events():
    global selected_tile
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            current_player = game.players[game.current_player_index]
            
            # Draw tile from the pool
            if 10 <= x <= 10 + TILE_WIDTH and 10 <= y <= 10 + TILE_HEIGHT:
                Game.draw_tile(current_player)
            
            # Click on a tile in the player's hand
            for i, tile in enumerate(current_player.hand):
                tile_x = 100 + i * TILE_WIDTH
                tile_y = 10 + game.current_player_index * 80
                if tile_x <= x <= tile_x + TILE_WIDTH and tile_y <= y <= tile_y + TILE_HEIGHT:
                    selected_tile = tile  # Select the tile
            
            # Click on the board to place the selected tile
            if selected_tile:
                game.board.add_tile(selected_tile)  
                current_player.hand.remove(selected_tile)
                selected_tile = None
    

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    handle_events()
    draw_tiles()
    
    # Check for game over condition 
    if game.game_over():
        running = False
    
    # Change turn on space key press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        game.next_turn()

pygame.quit()