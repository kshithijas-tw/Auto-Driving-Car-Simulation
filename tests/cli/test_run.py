import pytest
from cli.run import read_car, print_cars, run_simulation
from domain.car import Car
from domain.position import Position
from domain.direction import Direction
from domain.field import Field


def test_read_car_valid_input(monkeypatch):
    inputs = iter([
        "A",
        "1 2 N",
        "FFR"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    car = read_car(existing_names=set())

    assert isinstance(car, Car)
    assert car.name == "A"
    assert car.position == Position(1, 2)
    assert car.direction == Direction.N
    assert car.commands == ["F", "F", "R"]


def test_read_car_duplicate_name(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "A")

    with pytest.raises(ValueError):
        read_car(existing_names={"A"})


def test_read_car_invalid_direction(monkeypatch):
    inputs = iter([
        "A",
        "1 2 X",
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(ValueError):
        read_car(existing_names=set())

def test_print_cars(capsys):
    cars = [
        Car("A", Position(1, 2), Direction.N, "FF"),
        Car("B", Position(3, 4), Direction.E, "L"),
    ]

    print_cars(cars)

    captured = capsys.readouterr().out

    assert "Your current list of cars are" in captured
    assert "- A, (1,2) N, FF" in captured
    assert "- B, (3,4) E, L" in captured

def test_run_simulation_single_car_no_collision(capsys):
    field = Field(10, 10)
    cars = [
        Car("A", Position(1, 2), Direction.N, "FF")
    ]

    run_simulation(field, cars)

    output = capsys.readouterr().out

    assert "After simulation, the result is:" in output
    assert "- A, (1,4) N" in output

def test_run_simulation_with_collision(capsys):
    field = Field(10, 10)

    car_a = Car("A", Position(1, 2), Direction.N, "FFRFFFFRRL")
    car_b = Car("B", Position(7, 8), Direction.W, "FFLFFFFFFF")

    run_simulation(field, [car_a, car_b])

    output = capsys.readouterr().out

    assert "collides with" in output
    assert "at step 7" in output
    assert "(5,4)" in output