import math
import random

import pytest
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from Entities.ball import Ball
from Entities.enemy import Enemy
from Entities.mass import Mass
from Entities.player import Player
from Entities.power_ups import Power_Up
from Game_Control.Vector import Vector
from Game_Control.interactions import Interaction
from Game_Control.keyboard import Keyboard
from Maps.line import Line
from tests.conftest import DummyCanvas, DummyTimer


def test_dummy_timer_and_canvas_helpers():
    calls: list[str] = []
    timer = DummyTimer(50, lambda: calls.append("tick"))

    timer.trigger()

    assert calls == ["tick"]
    canvas = DummyCanvas()
    canvas.draw_line((0, 0), (1, 1), 2, "c")
    assert canvas.calls[-1][0] == "line"


def test_line_draw_invokes_canvas(dummy_canvas):
    line = Line(Vector(0, 0), Vector(1, 0))

    line.draw(dummy_canvas)

    assert ("line", ((0, 0), (1, 0), 30, "white")) in dummy_canvas.calls


def test_vector_additional_operations():
    vector = Vector(1, 2)

    assert str(vector) == "(1,2)"
    assert vector.__eq__("x") is NotImplemented
    scaled = vector * 2
    assert scaled == Vector(2, 4)
    divided = scaled / 2
    assert divided == Vector(1, 2)
    assert divided.length_squared() == pytest.approx(5)
    assert Vector(1, 0).angle(Vector(0, 1)) == pytest.approx(math.pi / 2)
    rotated = Vector(1, 0).rotate_rad(math.pi / 2)
    assert rotated.x == pytest.approx(0, abs=1e-9)
    assert rotated.y == pytest.approx(1)
    rotated_deg = Vector(0, 1).rotate(90)
    assert rotated_deg.x == pytest.approx(-1)
    assert rotated_deg.y == pytest.approx(0, abs=1e-9)


def test_keyboard_tracks_left_and_down():
    keyboard = Keyboard()

    keyboard.keyDown(simplegui.KEY_MAP["left"])
    keyboard.keyDown(simplegui.KEY_MAP["down"])
    assert keyboard.left is True
    assert keyboard.down is True

    keyboard.keyUp(simplegui.KEY_MAP["left"])
    keyboard.keyUp(simplegui.KEY_MAP["down"])
    assert keyboard.left is False
    assert keyboard.down is False


def test_draw_covers_all_entities(interaction_factory, dummy_canvas):
    interaction: Interaction = interaction_factory()
    interaction.mass.append(Mass(Vector(70, 70), Vector(0, 0), 1))
    interaction.power_ups.append(Power_Up(Vector(80, 60)))

    interaction.draw(dummy_canvas)
    interaction.time_limit = -1
    interaction.draw_score(dummy_canvas)
    assert any(call[0] == "circle" for call in dummy_canvas.calls)
    assert any(call[0] == "line" for call in dummy_canvas.calls)
    assert any(call[0] == "text" for call in dummy_canvas.calls)


def test_player_controls_with_speed_power_up(interaction_factory):
    player = Player(Vector(10, 10), Vector(0, 0), 20)
    keyboard = Keyboard()
    keyboard.right = True
    keyboard.left = True
    keyboard.up = True
    keyboard.down = True
    interaction = interaction_factory(player=player, keyboard=keyboard)
    interaction.player.power_up = "Speed"

    interaction.player_controls()

    assert interaction.player.velocity == Vector(0, 0)
    assert len(interaction.mass) == 4
    assert interaction.player.radius == pytest.approx(19.2)


def test_update_enemy_handles_collisions(interaction_factory):
    player = Player(Vector(0, 0), Vector(0, 0), 1)
    enemy1 = Enemy(Vector(0, 0), Vector(0, 0), 5)
    enemy2 = Enemy(Vector(0, 0), Vector(0, 0), 4)
    mass = Mass(Vector(0, 0), Vector(0, 0), 1)
    interaction = interaction_factory(player=player, enemies=[enemy1, enemy2])
    interaction.mass = [mass]

    interaction.update_enemy()

    assert player.alive is False
    assert len(interaction.enemy) == 1
    assert interaction.enemy[0].radius == pytest.approx(11)
    assert interaction.mass == []


def test_enemy_split_handles_vertical_velocity(interaction_factory):
    random.seed(1)
    enemy = Enemy(Vector(50, 50), Vector(0, 1), 20)
    interaction = interaction_factory(enemies=[enemy])

    interaction.enemy_split()

    assert len(interaction.enemy) == 2
    new_enemy = [e for e in interaction.enemy if e is not enemy][0]
    assert new_enemy.velocity.x == pytest.approx(1)


def test_update_mass_engulfs_on_collision(interaction_factory):
    player = Player(Vector(0, 0), Vector(0, 0), 10)
    mass = Mass(Vector(0, 0), Vector(0, 0), 1)
    interaction = interaction_factory(player=player)
    interaction.mass = [mass]

    interaction.update_mass()

    assert interaction.mass == []
    assert interaction.player.radius > 10


def test_update_power_ups_grants_speed(interaction_factory):
    player = Player(Vector(0, 0), Vector(0, 0), 10)
    power = Power_Up(Vector(0, 0))
    interaction = interaction_factory(player=player)
    interaction.power_ups = [power]

    interaction.update_power_ups()

    assert interaction.power_ups == []
    assert interaction.player.power_up == "Speed"
    assert interaction.player_power_up_timer.started is True


def test_bounce_without_collision_resets_flag(interaction_factory):
    interaction = interaction_factory()
    ball = Ball(Vector(50, 40), Vector(0, 0), 1)
    ball.in_collision = True

    interaction.bounce(ball)

    assert ball.in_collision is False


def test_game_finish_handles_player_death(interaction_factory, simplegui_stub, frame_stub):
    interaction = interaction_factory(frame=frame_stub)
    interaction.player.alive = False

    interaction.game_finish()

    assert frame_stub.stopped is True
    assert all(timer.stop_calls == 1 for timer in simplegui_stub.timers)


def test_game_finish_handles_timeout(interaction_factory, simplegui_stub, frame_stub):
    interaction = interaction_factory(time_limit=0, frame=frame_stub)

    interaction.game_finish()

    assert frame_stub.stopped is True
    assert all(timer.stop_calls == 1 for timer in simplegui_stub.timers)


def test_game_finish_handles_exit_key(interaction_factory, simplegui_stub, frame_stub):
    keyboard = Keyboard()
    keyboard.e = True
    interaction = interaction_factory(keyboard=keyboard, frame=frame_stub, time_limit=5)

    interaction.game_finish()

    assert frame_stub.stopped is True
    assert all(timer.stop_calls == 1 for timer in simplegui_stub.timers)
