from game.models.components.ship import Ship


class Cell:
    def __init__(self):
        self.hit = False

    def is_hit(self) -> bool:
        return self.hit

    def set_hit(self, hit: bool):
        self.hit = hit


class CellWithShip(Cell):
    def __init__(self, ship: Ship):
        super().__init__()
        self.ship = ship

    def get_ship(self) -> Ship:
        return self.ship
