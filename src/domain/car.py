from domain.direction import Direction
from domain.position import Position
from domain.field import Field


class Car:
    def __init__(self, name: str, position: Position, direction: Direction, commands: str):
        self.name = name
        self.position = position
        self.direction = direction
        self.commands = list(commands)

    def has_commands_left(self) -> bool:
        return len(self.commands) > 0

    def peek_next_state(self, field: Field) -> tuple[Position, Direction]:
        if not self.has_commands_left():
            return self.position, self.direction

        command = self.commands[0]

        if command == "L":
            return self.position, self.direction.left()

        if command == "R":
            return self.position, self.direction.right()

        if command == "F":
            dx, dy = self.direction.forward_delta()
            new_position = self.position.move(dx, dy)

            if field.is_within_bounds(new_position):
                return new_position, self.direction

        return self.position, self.direction

    def commit(self, position: Position, direction: Direction) -> None:
        if not self.has_commands_left():
            return

        self.commands.pop(0)
        self.position = position
        self.direction = direction
