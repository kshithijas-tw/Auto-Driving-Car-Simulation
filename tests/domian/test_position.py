from domain.position import Position


def test_position_creation():
    pos = Position(1, 2)
    assert pos.x == 1
    assert pos.y == 2


def test_position_move_returns_new_instance():
    pos = Position(1, 2)
    new_pos = pos.move(1, -1)

    assert new_pos.x == 2
    assert new_pos.y == 1


def test_position_is_immutable():
    pos = Position(1, 2)
    new_pos = pos.move(0, 1)

    assert pos.x == 1
    assert pos.y == 2
    assert new_pos != pos


def test_position_equality():
    assert Position(3, 4) == Position(3, 4)
    assert Position(3, 4) != Position(4, 3)
