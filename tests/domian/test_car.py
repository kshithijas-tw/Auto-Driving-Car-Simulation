from domain.car import Car
from domain.position import Position
from domain.direction import Direction
from domain.field import Field


def test_car_turns_left():
    car = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="L",
    )

    new_pos, new_dir = car.peek_next_state(Field(10, 10))
    car.commit(new_pos, new_dir)

    assert car.direction == Direction.W
    assert car.position == Position(1, 2)


def test_car_turns_right():
    car = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="R",
    )

    new_pos, new_dir = car.peek_next_state(Field(10, 10))
    car.commit(new_pos, new_dir)

    assert car.direction == Direction.E


def test_car_moves_forward_within_bounds():
    car = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="F",
    )

    new_pos, new_dir = car.peek_next_state(Field(10, 10))
    car.commit(new_pos, new_dir)

    assert car.position == Position(1, 3)


def test_car_ignores_move_out_of_bounds():
    car = Car(
        name="A",
        position=Position(0, 0),
        direction=Direction.S,
        commands="F",
    )

    new_pos, new_dir = car.peek_next_state(Field(10, 10))
    car.commit(new_pos, new_dir)

    assert car.position == Position(0, 0)


def test_car_no_commands_left():
    car = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="",
    )

    new_pos, new_dir = car.peek_next_state(Field(10, 10))
    car.commit(new_pos, new_dir)

    assert car.position == Position(1, 2)
    assert car.direction == Direction.N

def test_car_proposes_forward_move():
    car = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="F",
    )

    new_pos, new_dir = car.peek_next_state(Field(10, 10))

    assert new_pos == Position(1, 3)
    assert new_dir == Direction.N


def test_car_proposes_turn_only():
    car = Car(
        name="A",
        position=Position(1, 2),
        direction=Direction.N,
        commands="L",
    )

    new_pos, new_dir = car.peek_next_state(Field(10, 10))

    assert new_pos == Position(1, 2)
    assert new_dir == Direction.W
