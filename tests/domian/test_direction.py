import pytest
from domain.direction import Direction


def test_turn_left_from_north():
    assert Direction.N.left() == Direction.W


def test_turn_right_from_north():
    assert Direction.N.right() == Direction.E


def test_turn_left_from_east():
    assert Direction.E.left() == Direction.N


def test_turn_right_from_west():
    assert Direction.W.right() == Direction.N


@pytest.mark.parametrize(
    "direction, expected_delta",
    [
        (Direction.N, (0, 1)),
        (Direction.E, (1, 0)),
        (Direction.S, (0, -1)),
        (Direction.W, (-1, 0)),
    ],
)
def test_forward_delta(direction, expected_delta):
    assert direction.forward_delta() == expected_delta
