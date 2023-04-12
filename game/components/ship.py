
class Ship:
    def __init__(self, width: int, length: int):
        self.width = width
        self.length = length
        self.size = width * length
        self.hits = 0

    def is_sunk(self) -> bool:
        return self.hits == self.size