from domain.field import Field
from domain.position import Position


def test_position_inside_bounds():
    field = Field(10, 10)
    assert field.is_within_bounds(Position(0, 0))
    assert field.is_within_bounds(Position(9, 9))


def test_position_outside_bounds():
    field = Field(10, 10)
    assert not field.is_within_bounds(Position(-1, 0))
    assert not field.is_within_bounds(Position(0, -1))
    assert not field.is_within_bounds(Position(10, 0))
    assert not field.is_within_bounds(Position(0, 10))


def test_field_with_size_one():
    field = Field(1, 1)
    assert field.is_within_bounds(Position(0, 0))
    assert not field.is_within_bounds(Position(1, 0))
