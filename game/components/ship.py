
class Ship:
    def __init__(self, pos: (int, int), width: int,
                 length: int, horizontal=False):
        self.pos = pos
        self.width = width
        self.length = length
        self.horizontal = horizontal
        self.size = width * length
        self.hits = 0

    def is_sunk(self) -> bool:
        return self.hits == self.size

    def set_horizontal(self, value: bool):
        self.horizontal = value