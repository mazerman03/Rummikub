from source.game import Game

def main():
    #TODO: Runs with default names, player number and names be custom.
    game = Game(player_names=["Noe", "Max", "Will"])
    while not game.game_over():
        game.play_turn()

    print("\nGame Over!")

    #TODO: Implement a scoreboard with the points for each player.  
    for player in game.players:
        print(f"{player.name}'s remaining tiles: {player.hand}")

if __name__ == "__main__":
    main()

