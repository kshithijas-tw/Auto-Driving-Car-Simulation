from domain.car import Car
from domain.position import Position
from domain.direction import Direction


class MoveProposal:
    from_position: Position
    to_position: Position
    from_direction: Direction
    to_direction: Direction

    def __init__(self, from_position: Position, to_position: Position, from_direction: Direction, to_direction: Direction):
        self.from_position = from_position
        self.to_position = to_position
        self.from_direction = from_direction
        self.to_direction = to_direction


class Collision:
    position: Position
    step: int
    cars: list[Car]
    type: str = "same_tile"

    def __init__(self, position: Position, step: int, cars: list[Car], type: str = "same_tile"):    
        self.position = position
        self.step = step
        self.cars = cars
        self.type = type