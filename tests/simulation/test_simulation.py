from domain.position import Position
from domain.direction import Direction
from domain.field import Field
from domain.car import Car
from simulation.simulation import StepByStepSimulation


def test_single_car_simulation():
    field = Field(10, 10)
    car = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="FFRFFFFRRL",
    )

    simulation = StepByStepSimulation(field, [car])
    simulation.run()

    assert car.position == Position(5, 4)
    assert car.direction == Direction.S

def test_two_cars_move_step_by_step_without_collision():
    field = Field(10, 10)

    car_a = Car(
        name="A",
        position=Position(0, 0),
        direction=Direction.N,
        commands="FF",
    )

    car_b = Car(
        name="B",
        position=Position(9, 9),
        direction=Direction.S,
        commands="F",
    )

    simulation = StepByStepSimulation(field, [car_a, car_b])
    simulation.run()

    assert car_a.position == Position(0, 2)
    assert car_b.position == Position(9, 8)

def test_two_cars_collide():
    field = Field(10, 10)

    car_a = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="FFRFFFFRRL",
    )

    car_b = Car(
        name="B",
        position=Position(7, 8),
        direction=Direction.W,
        commands="FFLFFFFFFF",
    )

    simulation = StepByStepSimulation(field, [car_a, car_b])
    result = simulation.run()

    assert result["collisions"][0].position == Position(5, 4)
    assert result["collisions"][0].step == 7
