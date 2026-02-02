from typing import Any

from domain.field import Field
from domain.car import Car
from domain.position import Position
from domain.direction import Direction


class Simulation:
    def __init__(self, field: Field, cars: list[Car]):
        self.field = field
        self.cars = cars
        self.step = 0
        self.collisions: list[dict[str, Any]] = []
        

    def _has_collisions(self, proposals: dict[Position, list[tuple[Car, Direction]]]) -> bool:
        collided_positions = {
            pos: cars for pos, cars in proposals.items() if len(cars) > 1
        }
        if collided_positions:
            for pos, cars in collided_positions.items():
                self.collisions.append({
                    "position": pos,
                    "step": self.step,
                    "cars": [c.name for c, _ in cars]
                })
                return True
        return False

    def run(self) -> dict[str, Any]:
        while True:
            self.step += 1
            proposals = {}

            for car in self.cars:
                if car.has_commands_left():
                    pos, dir_ = car.peek_next_state(self.field)
                    proposals.setdefault(pos, []).append((car, dir_))

            if self._has_collisions(proposals):
                break

            moved = False
            for pos, cars in proposals.items():
                for car, dir_ in cars:
                    car.commit(pos, dir_)
                    moved = True

            if not moved:
                break

        return {"collisions": self.collisions}
