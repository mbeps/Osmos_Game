import pytest

from Game_Control.Vector import Vector


def test_add_subtract_and_equality() -> None:
    v1: Vector = Vector(1, 2)
    v2: Vector = Vector(3, 4)

    assert v1 + v2 == Vector(4, 6)
    assert v2 - v1 == Vector(2, 2)
    assert v1 != v2


def test_length_and_normalize() -> None:
    vector: Vector = Vector(3, 4)

    assert vector.length() == pytest.approx(5)
    unit: Vector = vector.get_normalized()
    assert unit.length() == pytest.approx(1)
    assert unit.x == pytest.approx(0.6)
    assert unit.y == pytest.approx(0.8)


def test_reflect_and_rotate() -> None:
    reflected: Vector = Vector(1, -1).reflect(Vector(0, 1))
    assert reflected == Vector(1, 1)

    rotated: Vector = Vector(2, 0).rotate_anti()
    assert rotated == Vector(0, 2)


def test_projection() -> None:
    base: Vector = Vector(3, 4)
    projection: Vector = base.get_proj(Vector(1, 0))
    assert projection == Vector(3, 0)
