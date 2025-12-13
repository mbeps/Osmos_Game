from Entities.ball import Ball
from Entities.enemy import Enemy
from Entities.mass import Mass
from Entities.player import Player
from Entities.power_ups import Power_Up
from Game_Control.Vector import Vector


def test_ball_update_bounce_and_radius(dummy_canvas):
    ball = Ball(Vector(0, 0), Vector(1, 2), 6)

    ball.update()
    assert ball.position == Vector(1, 2)

    ball.bounce(Vector(1, 0))
    assert ball.velocity == Vector(-1, 2)

    ball.set_radius(10)
    assert ball.radius == 10


def test_ball_draw_records_canvas_calls(dummy_canvas):
    ball = Ball(Vector(5, 5), Vector(0, 0), 6)
    ball.draw(dummy_canvas)

    methods = [call[0] for call in dummy_canvas.calls]
    assert "circle" in methods
    assert "point" in methods
    text_calls = [call for call in dummy_canvas.calls if call[0] == "text"]
    assert text_calls
    assert text_calls[0][1][0] == str(round(ball.radius))


def test_entity_initialisation_and_draw(dummy_canvas):
    position = Vector(1, 1)
    velocity = Vector(1, 0)

    enemy = Enemy(position.copy(), velocity.copy(), 10)
    assert enemy.type == "Enemy"
    assert enemy.colour == "Red"

    mass = Mass(position.copy(), velocity.copy(), 0.5)
    assert mass.type == "Mass"
    assert mass.colour == "Aqua"
    assert mass.radius == 0.5
    mass.draw(dummy_canvas)
    mass_circle = [call for call in dummy_canvas.calls if call[0] == "circle"][-1]
    assert mass_circle[1][1] == 2

    player = Player(position.copy(), velocity.copy(), 12)
    player.can_move()
    assert player.move is True
    player.set_radius(8)
    player.can_move()
    assert player.move is False
    player.set_radius(14)
    player.can_move()
    assert player.move is True

    power_up = Power_Up(position.copy())
    assert power_up.type == "Power_Up"
    assert power_up.colour == "Yellow"
    assert power_up.velocity == Vector(0, 0)
