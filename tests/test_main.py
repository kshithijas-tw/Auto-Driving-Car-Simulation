import types

import pytest

import main as main_module


def make_dummy_field(width=5, height=6):
    return types.SimpleNamespace(width=width, height=height)


def test_main_add_car_and_run_simulation_exit(monkeypatch, capsys):
    field = make_dummy_field()
    car = object()

    monkeypatch.setattr(main_module, "read_field", lambda: field)
    monkeypatch.setattr(main_module, "read_car", lambda existing_names: car)

    printed_cars = {}

    def fake_print_cars(cars):
        printed_cars["cars"] = list(cars)

    called = {}

    def fake_run_simulation(f, cars):
        called["field"] = f
        called["cars"] = list(cars)

    monkeypatch.setattr(main_module, "print_cars", fake_print_cars)
    monkeypatch.setattr(main_module, "run_simulation", fake_run_simulation)

    inputs = iter(
        [
            "1", "2", "2", 
        ]
    )
    monkeypatch.setattr("builtins.input", lambda: next(inputs))

    main_module.main()

    assert printed_cars["cars"] == [car]

    assert called["field"] is field
    assert called["cars"] == [car]

    out = capsys.readouterr().out
    assert "You have created a field of 5 x 6." in out


def test_main_invalid_choice_then_exit(monkeypatch, capsys):
    field = make_dummy_field()
    monkeypatch.setattr(main_module, "read_field", lambda: field)

    def fake_run_simulation(f, cars):
        return

    monkeypatch.setattr(main_module, "run_simulation", fake_run_simulation)
    monkeypatch.setattr(main_module, "read_car", lambda existing_names: object())
    monkeypatch.setattr(main_module, "print_cars", lambda cars: None)

    inputs = iter(
        [
            "9", "2",
            "2",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda: next(inputs))

    main_module.main()

    out = capsys.readouterr().out
    assert "Invalid choice." in out


def test_main_add_car_error(monkeypatch, capsys):
    field = make_dummy_field()
    monkeypatch.setattr(main_module, "read_field", lambda: field)

    def bad_read_car(existing_names):
        raise ValueError("bad car")

    monkeypatch.setattr(main_module, "read_car", bad_read_car)

    run_args = {}

    def fake_run_simulation(f, cars):
        run_args["field"] = f
        run_args["cars"] = list(cars)

    monkeypatch.setattr(main_module, "run_simulation", fake_run_simulation)
    monkeypatch.setattr(main_module, "print_cars", lambda cars: None)

    inputs = iter(
        [
            "1", "2", 
            "2", 
        ]
    )
    monkeypatch.setattr("builtins.input", lambda: next(inputs))

    main_module.main()

    out = capsys.readouterr().out
    assert "Error: bad car" in out

    assert run_args["field"] is field
    assert run_args["cars"] == []


def test_main_start_over_calls_main_again(monkeypatch, capsys):
    field = make_dummy_field()
    monkeypatch.setattr(main_module, "read_field", lambda: field)
    monkeypatch.setattr(main_module, "read_car", lambda existing_names: object())
    monkeypatch.setattr(main_module, "print_cars", lambda cars: None)
    monkeypatch.setattr(main_module, "run_simulation", lambda f, cars: None)

    calls = []

    real_main = main_module.main

    def fake_main():
        calls.append("called-again")
    monkeypatch.setattr(main_module, "main", fake_main)

    inputs = iter(
        [
            "2",
            "1",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda: next(inputs))

    real_main()

    assert calls == ["called-again"]

