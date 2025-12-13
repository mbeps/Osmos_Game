import pytest
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from Entities.ball import Ball
from Game_Control.keyboard import Keyboard
from Game_Control.Vector import Vector
from Maps.line import Line


def test_line_distance_computation():
    line = Line(Vector(0, 0), Vector(0, 10))
    ball = Ball(Vector(5, 5), Vector(0, 0), 1)

    assert line.distance(ball) == pytest.approx(5)


def test_keyboard_tracks_keypresses():
    keyboard = Keyboard()

    keyboard.keyDown(simplegui.KEY_MAP["right"])
    keyboard.keyDown(simplegui.KEY_MAP["up"])
    keyboard.keyDown(simplegui.KEY_MAP["e"])
    assert keyboard.right is True
    assert keyboard.up is True
    assert keyboard.e is True

    keyboard.keyUp(simplegui.KEY_MAP["right"])
    keyboard.keyUp(simplegui.KEY_MAP["up"])
    keyboard.keyUp(simplegui.KEY_MAP["e"])
    assert keyboard.right is False
    assert keyboard.up is False
    assert keyboard.e is False
