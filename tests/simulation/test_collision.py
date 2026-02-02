from domain.position import Position
from domain.direction import Direction
from domain.field import Field
from domain.car import Car
from domain.events import MoveProposal, Collision
from simulation.collision import SameTileCollisionDetector
from simulation.simulation import Simulation


def _make_car(name: str, x: int, y: int, direction: Direction, commands: str) -> Car:
    return Car(
        name=name,
        position=Position(x, y),
        direction=direction,
        commands=commands,
    )


def test_same_tile_collision_detector_detects_multiple_cars_on_same_tile():
    detector = SameTileCollisionDetector()

    car_a = _make_car("A", 0, 0, Direction.N, "F")
    car_b = _make_car("B", 1, 0, Direction.W, "F")

    to_position = Position(1, 1)
    proposals_by_position = {
        to_position: [
            MoveProposal(
                car=car_a,
                from_position=car_a.position,
                to_position=to_position,
                from_direction=car_a.direction,
                to_direction=car_a.direction,
            ),
            MoveProposal(
                car=car_b,
                from_position=car_b.position,
                to_position=to_position,
                from_direction=car_b.direction,
                to_direction=car_b.direction,
            ),
        ]
    }

    collisions = detector.detect(step=3, proposals_by_position=proposals_by_position)

    assert len(collisions) == 1
    collision = collisions[0]
    assert collision.position == to_position
    assert collision.step == 3
    assert {car.name for car in collision.cars} == {"A", "B"}


def test_custom_collision_detector_can_be_injected_into_simulation():
    class AlwaysCollideDetector(SameTileCollisionDetector):
        def detect(self, step, proposals_by_position):
            
            fake_position = Position(0, 0)
            return [
                Collision(
                    position=fake_position,
                    step=step,
                    cars=[],
                )
            ]

    field = Field(5, 5)
    car = _make_car("A", 1, 1, Direction.N, "FF")

    simulation = Simulation(field, [car], collision_detector=AlwaysCollideDetector())
    result = simulation.run()

    assert result["collisions"][0]["position"] == Position(0, 0)
    assert result["collisions"][0]["step"] == 1
    assert car.position == Position(1, 1)

