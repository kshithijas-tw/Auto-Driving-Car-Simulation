from dataclasses import dataclass

from domain.car import Car
from domain.position import Position
from domain.direction import Direction


@dataclass(frozen=True)
class MoveProposal:
    car: Car
    from_position: Position
    to_position: Position
    from_direction: Direction
    to_direction: Direction


@dataclass
class Collision:
    position: Position
    step: int
    cars: list[Car]
    type: str = "same_tile"

