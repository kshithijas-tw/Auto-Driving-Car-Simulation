from domain.field import Field
from domain.car import Car
from domain.position import Position
from domain.direction import Direction
from simulation.simulation import Simulation


def read_field():
    print("Welcome to Auto Driving Car Simulation!\n")
    while True:
        try:
            w, h = map(int, input(
                "Please enter the width and height of the simulation field in x y format:\n"
            ).split())
            return Field(w, h)
        except ValueError:
            print("Invalid input. Please enter two numbers.")


def read_car(existing_names):
    name = input("Please enter the name of the car:\n").strip()
    if name in existing_names:
        raise ValueError("Car name must be unique")

    x, y, d = input(
        f"Please enter initial position of car {name} in x y Direction format:\n"
    ).split()

    if d not in {"N", "S", "E", "W"}:
        raise ValueError("Invalid direction")

    commands = input(f"Please enter the commands for car {name}:\n").strip()

    return Car(
        name=name,
        position=Position(int(x), int(y)),
        direction=Direction[d],
        commands=commands,
    )


def print_cars(cars):
    print("\nYour current list of cars are:")
    for car in cars:
        print(
            f"- {car.name}, ({car.position.x},{car.position.y}) "
            f"{car.direction.name}, {''.join(car.commands)}"
        )
    print()


def run_simulation(field, cars):
    print_cars(cars)

    simulation = Simulation(field, cars)
    result = simulation.run()
    collisions = result["collisions"]

    print("After simulation, the result is:")
    for car in cars:
        collision = next((collision for collision in collisions if car in collision.cars), None)
        if car.has_collided() and collision:
            others = ", ".join([c.name for c in collision.cars if c.name != car.name])
            print(f"- {car.name}, collides with {others} at "
                    f"({collision.position.x},{collision.position.y}) at step {collision.step}")
        else:
            print(f"- {car.name}, ({car.position.x},{car.position.y}) {car.direction.name}")
    print("\n")

