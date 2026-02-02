from enum import Enum


class Direction(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def left(self) -> "Direction":
        directions = list(Direction)
        return directions[(directions.index(self) - 1) % len(directions)]

    def right(self) -> "Direction":
        directions = list(Direction)
        return directions[(directions.index(self) + 1) % len(directions)]

    def forward_delta(self) -> tuple[int, int]:
        return {
            Direction.N: (0, 1),
            Direction.E: (1, 0),
            Direction.S: (0, -1),
            Direction.W: (-1, 0),
        }[self]
