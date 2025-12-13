import random
import types
from collections.abc import Callable

import pytest

from Entities.ball import Ball
from Entities.enemy import Enemy
from Entities.player import Player
from Entities.power_ups import Power_Up
from Game_Control.interactions import Interaction
from Game_Control.keyboard import Keyboard
from Game_Control.Vector import Vector
from Maps.line import Line
from tests.conftest import DummyFrame

InteractionFactory = Callable[..., Interaction]


def test_hit_ball_detects_collision(
    interaction_factory: InteractionFactory,
) -> None:
    interaction: Interaction = interaction_factory()
    ball1: Ball = Ball(Vector(0, 0), Vector(0, 0), 5)
    ball2: Ball = Ball(Vector(9, 0), Vector(0, 0), 5)

    assert interaction.hit_ball(ball1, ball2) is True
    ball2.position = Vector(11, 0)
    assert interaction.hit_ball(ball1, ball2) is False


def test_engulf_updates_enemy_list_and_score(
    interaction_factory: InteractionFactory,
) -> None:
    player: Player = Player(Vector(50, 50), Vector(0, 0), 12)
    enemy: Enemy = Enemy(Vector(60, 50), Vector(0, 0), 5)
    interaction: Interaction = interaction_factory(player=player, enemies=[enemy])

    interaction.engulf(player, enemy)

    assert enemy not in interaction.enemy
    assert interaction.kill_counter == 1
    assert player.radius == pytest.approx(17)


def test_engulf_when_player_is_smaller_marks_player_dead(
    interaction_factory: InteractionFactory,
) -> None:
    player: Player = Player(Vector(10, 10), Vector(0, 0), 5)
    enemy: Enemy = Enemy(Vector(12, 10), Vector(0, 0), 10)
    interaction: Interaction = interaction_factory(player=player, enemies=[enemy])

    interaction.engulf(enemy, player)

    assert player.alive is False
    assert enemy.radius == pytest.approx(15)


def test_bounce_reflects_velocity_against_wall(
    interaction_factory: InteractionFactory,
) -> None:
    left_wall: Line = Line(Vector(0, 0), Vector(0, 50))
    interaction: Interaction = interaction_factory(lines=[left_wall])
    ball: Ball = Ball(Vector(1, 10), Vector(-2, 0), 5)

    interaction.bounce(ball)

    assert ball.velocity == Vector(2, 0)
    assert ball.in_collision is True


def test_gravity_moves_smaller_ball_towards_larger(
    interaction_factory: InteractionFactory,
) -> None:
    small: Ball = Ball(Vector(0, 0), Vector(0, 0), 5)
    large: Ball = Ball(Vector(10, 0), Vector(0, 0), 15)
    interaction: Interaction = interaction_factory()

    interaction.gravity(small, large)

    assert small.velocity.x > 0
    assert small.velocity.x == pytest.approx(10 / 700)
    assert small.velocity.y == pytest.approx(0)
    assert large.velocity.x == pytest.approx(-10 / (700 * 5))
    assert large.velocity.y == pytest.approx(0)


def test_enemy_split_creates_new_enemy_and_adjusts_radius(
    interaction_factory: InteractionFactory,
) -> None:
    random.seed(0)
    enemy: Enemy = Enemy(Vector(50, 50), Vector(1, 0), 20)
    interaction: Interaction = interaction_factory(enemies=[enemy])

    interaction.enemy_split()

    assert len(interaction.enemy) == 2
    radii: list[float] = sorted([e.radius for e in interaction.enemy])
    assert radii == [9, 11]
    new_enemy: Enemy = [e for e in interaction.enemy if e.radius == 11][0]
    assert new_enemy.velocity.x == pytest.approx(-1.5)
    assert new_enemy.velocity.y == pytest.approx(1.0)
    assert new_enemy.position.x == pytest.approx(24.2064408755)
    assert new_enemy.position.y == pytest.approx(67.1957060829)


def test_add_power_up_respects_limit(
    interaction_factory: InteractionFactory,
) -> None:
    interaction: Interaction = interaction_factory()
    interaction.power_ups = [
        Power_Up(Vector(0, 0)),
        Power_Up(Vector(0, 0)),
        Power_Up(Vector(0, 0)),
        Power_Up(Vector(0, 0)),
        Power_Up(Vector(0, 0)),
    ]

    interaction.add_power_up()
    assert len(interaction.power_ups) == 5

    interaction.power_ups = []
    random.seed(1)
    interaction.add_power_up()
    assert len(interaction.power_ups) == 1
    position: Vector = interaction.power_ups[0].position
    assert 5 <= position.x <= 790
    assert 5 <= position.y <= 490


def test_countdown_and_reset_power_up(
    interaction_factory: InteractionFactory,
) -> None:
    interaction: Interaction = interaction_factory(time_limit=3)
    interaction.player.power_up = "Speed"
    interaction.player_power_up_timer.start()

    interaction.countdown()
    assert interaction.time_limit == 2

    interaction.reset_player_power_up()
    assert interaction.player.power_up == "None"
    assert interaction.player_power_up_timer.started is False


def test_player_controls_ejects_mass_and_limits_velocity(
    interaction_factory: InteractionFactory,
) -> None:
    player: Player = Player(Vector(40, 40), Vector(0, 0), 20)
    keyboard: Keyboard = Keyboard()
    keyboard.right = True
    interaction: Interaction = interaction_factory(player=player, keyboard=keyboard)

    interaction.player_controls()

    assert interaction.player.velocity.x == 1
    assert len(interaction.mass) == 1
    assert interaction.mass[0].velocity == Vector(-1, 1)
    assert interaction.player.radius == pytest.approx(19.8)


def test_game_finish_stops_timers_on_win(
    interaction_factory: InteractionFactory,
    simplegui_stub: types.SimpleNamespace,
    frame_stub: DummyFrame,
) -> None:
    interaction: Interaction = interaction_factory()
    interaction.enemy.clear()

    interaction.game_finish()

    assert frame_stub.stopped is True
    # Four timers should all be stopped
    assert len(simplegui_stub.timers) == 4
    assert all(timer.stop_calls == 1 for timer in simplegui_stub.timers)
    assert all(timer.started is False for timer in simplegui_stub.timers)
