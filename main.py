# ^ MODULES:
import random
from typing import Literal

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from Entities.ball import Ball
from Entities.enemy import Enemy
from Entities.mass import Mass
from Entities.player import Player
from Game_Control.interactions import Interaction
from Game_Control.keyboard import Keyboard
from Game_Control.Vector import Vector
from Maps.line import Line

if __name__ == "__main__":
    # ^ Game Environment:
    canvas_dimensions: list[int] = [1456, 819]  # Default canvas size (16:9)
    time_limit: int = -1  # Default time is unlimited

    # ^ Entities:
    enemies: list[Enemy] = [
        Enemy(Vector(200, 150), Vector(-3, -3), 30),
        Enemy(Vector(700, 270), Vector(2, 4), 20),
        Enemy(Vector(400, 160), Vector(-2, 1), 15),
        Enemy(Vector(434, 112), Vector(1, 4), 10),
    ]
    player: Player = Player(
        Vector(canvas_dimensions[0] / 2, canvas_dimensions[1] - 100), Vector(0, 0), 40
    )

    frame: simplegui.Frame = simplegui.create_frame(
        "Domain", canvas_dimensions[0], canvas_dimensions[1]
    )
    lines: list[Line] = [
        Line(Vector(0, 0), Vector(0, canvas_dimensions[1])),  # Vertical 1
        Line(Vector(0, 0), Vector(canvas_dimensions[0], 0)),  # Horizontal 1
        Line(
            Vector(canvas_dimensions[0], 0),
            Vector(canvas_dimensions[0], canvas_dimensions[1]),
        ),  # Vertical 2
        Line(
            Vector(0, canvas_dimensions[1]),
            Vector(canvas_dimensions[0], canvas_dimensions[1]),
        ),
    ]  # Horizontal 2

    # ^ Backend:
    keyboard: Keyboard = Keyboard()
    interaction: Interaction = Interaction(
        lines, player, enemies, time_limit, keyboard, frame
    )

    # ^ Handlers:
    frame.set_draw_handler(interaction.draw)
    frame.set_keydown_handler(keyboard.keyDown)
    frame.set_keyup_handler(keyboard.keyUp)
    frame.add_button("Exit Game", interaction.stop)
    frame.start()  # Test
# Test
