import pytest

from Game_Control.Vector import Vector


def test_add_subtract_and_equality():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)

    assert v1 + v2 == Vector(4, 6)
    assert v2 - v1 == Vector(2, 2)
    assert v1 != v2


def test_length_and_normalize():
    vector = Vector(3, 4)

    assert vector.length() == pytest.approx(5)
    unit = vector.get_normalized()
    assert unit.length() == pytest.approx(1)
    assert unit.x == pytest.approx(0.6)
    assert unit.y == pytest.approx(0.8)


def test_reflect_and_rotate():
    reflected = Vector(1, -1).reflect(Vector(0, 1))
    assert reflected == Vector(1, 1)

    rotated = Vector(2, 0).rotate_anti()
    assert rotated == Vector(0, 2)


def test_projection():
    base = Vector(3, 4)
    projection = base.get_proj(Vector(1, 0))
    assert projection == Vector(3, 0)
