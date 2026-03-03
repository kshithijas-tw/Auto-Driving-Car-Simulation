from domain.position import Position
from domain.direction import Direction
from domain.field import Field
from domain.car import Car
from domain.events import MoveProposal, Collision
from simulation.collision import CollisionDetector
from simulation.simulation import StepByStepSimulation


def _make_car(name: str, x: int, y: int, direction: Direction, commands: str) -> Car:
    return Car(
        name=name,
        position=Position(x, y),
        direction=direction,
        commands=commands,
    )


def test_collision_detector_detects_multiple_cars_on_same_tile():
    detector = CollisionDetector()

    car_a = _make_car("A", 0, 0, Direction.N, "F")
    car_b = _make_car("B", 1, 0, Direction.W, "F")

    to_position = Position(1, 1)

    paths = {
        car_a: [
            MoveProposal(
                from_position=car_a.position,
                to_position=to_position,
                from_direction=car_a.direction,
                to_direction=car_a.direction,
            )
        ],
        car_b: [
            MoveProposal(
                from_position=car_b.position,
                to_position=to_position,
                from_direction=car_b.direction,
                to_direction=car_b.direction,
            )
        ],
    }

    collisions = detector.detect(step=3, paths=paths)

    assert len(collisions) == 1
    collision = collisions[0]
    assert collision.position == to_position
    assert collision.step == 3
    assert {car.name for car in collision.cars} == {"A", "B"}


def test_custom_collision_detector_can_be_injected_into_simulation():
    class AlwaysCollideDetector(CollisionDetector):
        def detect(self, step, paths):
            fake_position = Position(0, 0)
            cars = list(paths.keys())
            return [
                Collision(
                    position=fake_position,
                    step=step,
                    cars=cars,
                )
            ]

    field = Field(5, 5)
    car = _make_car("A", 1, 1, Direction.N, "FF")

    simulation = StepByStepSimulation(
        field, [car], collision_detector=AlwaysCollideDetector())
    result = simulation.run()

    assert result["collisions"][0].position == Position(0, 0)
    assert result["collisions"][0].step == 1
    assert car.position == Position(1, 1)


def test_collision_detector_adds_car_to_existing_collided_position():
    detector = CollisionDetector()

    # Step 1: two cars collide at the same tile
    car_a = _make_car("A", 0, 0, Direction.N, "F")
    car_b = _make_car("B", 0, 1, Direction.S, "F")
    collision_position = Position(0, 1)

    paths_step_1 = {
        car_a: [
            MoveProposal(
                from_position=car_a.position,
                to_position=collision_position,
                from_direction=car_a.direction,
                to_direction=car_a.direction,
            )
        ],
        car_b: [
            MoveProposal(
                from_position=car_b.position,
                to_position=collision_position,
                from_direction=car_b.direction,
                to_direction=car_b.direction,
            )
        ],
    }

    detector.detect(step=1, paths=paths_step_1)

    # Step 2: a third car moves into the already-collided position
    car_c = _make_car("C", 0, 2, Direction.S, "F")

    paths_step_2 = {
        car_c: [
            MoveProposal(
                from_position=car_c.position,
                to_position=collision_position,
                from_direction=car_c.direction,
                to_direction=car_c.direction,
            )
        ]
    }

    collisions = detector.detect(step=2, paths=paths_step_2)

    # The last collision should include all three cars at the same position
    last_collision = collisions[-1]
    assert last_collision.position == collision_position
    assert last_collision.step == 2
    assert {car.name for car in last_collision.cars} == {"A", "B", "C"}


def test_collision_detector_detects_swap_cycle_as_collision():
    detector = CollisionDetector()

    pos_a = Position(0, 0)
    pos_b = Position(1, 0)

    car_a = _make_car("A", pos_a.x, pos_a.y, Direction.E, "F")
    car_b = _make_car("B", pos_b.x, pos_b.y, Direction.W, "F")

    paths = {
        car_a: [
            MoveProposal(
                from_position=pos_a,
                to_position=pos_b,
                from_direction=car_a.direction,
                to_direction=car_a.direction,
            )
        ],
        car_b: [
            MoveProposal(
                from_position=pos_b,
                to_position=pos_a,
                from_direction=car_b.direction,
                to_direction=car_b.direction,
            )
        ],
    }

    collisions = detector.detect(step=1, paths=paths)

    cycle_collisions = [c for c in collisions if c.type == "cycle"]
    assert cycle_collisions, "Expected at least one cycle collision"

    cycle_collision = cycle_collisions[0]
    assert cycle_collision.position in {pos_a, pos_b}
    assert {car.name for car in cycle_collision.cars} == {"A", "B"}
