class Tile:
    #TODO: Again not including jokers, so might need to talk about how to implement them later on
    def __init__(self, color, number):
        self.color = color  
        self.number = number 

    def __repr__(self):
        return f"{self.color} {self.number}"

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.color == other.color and self.number == other.number
        return False
