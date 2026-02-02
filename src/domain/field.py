from domain.position import Position


class Field:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def is_within_bounds(self, position: Position) -> bool:
        return (
            0 <= position.x < self.width
            and 0 <= position.y < self.height
        )