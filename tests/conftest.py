import types

import pytest

import Game_Control.interactions as interactions


class DummyTimer:
    def __init__(self, interval, handler):
        self.interval = interval
        self.handler = handler
        self.started = False
        self.stop_calls = 0

    def start(self):
        self.started = True

    def stop(self):
        self.started = False
        self.stop_calls += 1

    def trigger(self):
        self.handler()


class DummyFrame:
    def __init__(self):
        self.stopped = False

    def stop(self):
        self.stopped = True


class DummyCanvas:
    def __init__(self):
        self.calls = []

    def draw_circle(self, *args):
        self.calls.append(("circle", args))

    def draw_point(self, *args):
        self.calls.append(("point", args))

    def draw_text(self, *args):
        self.calls.append(("text", args))

    def draw_line(self, *args):
        self.calls.append(("line", args))


@pytest.fixture
def dummy_canvas():
    return DummyCanvas()


@pytest.fixture
def simplegui_stub(monkeypatch):
    timers = []
    sg = types.SimpleNamespace()

    def create_timer(interval, handler):
        timer = DummyTimer(interval, handler)
        timers.append(timer)
        return timer

    sg.create_timer = create_timer
    sg.timers = timers
    monkeypatch.setattr(interactions, "simplegui", sg)
    return sg


@pytest.fixture
def frame_stub():
    return DummyFrame()


@pytest.fixture
def lines_square():
    from Game_Control.Vector import Vector
    from Maps.line import Line

    width, height = 100, 80
    return [
        Line(Vector(0, 0), Vector(width, 0)),
        Line(Vector(width, 0), Vector(width, height)),
        Line(Vector(0, height), Vector(width, height)),
        Line(Vector(0, 0), Vector(0, height)),
    ]


@pytest.fixture
def interaction_factory(simplegui_stub, frame_stub, lines_square):
    from Entities.enemy import Enemy
    from Entities.player import Player
    from Game_Control.interactions import Interaction
    from Game_Control.keyboard import Keyboard
    from Game_Control.Vector import Vector

    def factory(
        player=None,
        enemies=None,
        time_limit=10,
        keyboard=None,
        lines=None,
        frame=None,
    ):
        player_obj = player or Player(Vector(10, 10), Vector(0, 0), 20)
        enemies_list = enemies or [Enemy(Vector(30, 30), Vector(1, 0), 5)]
        keyboard_obj = keyboard or Keyboard()
        frame_obj = frame or frame_stub
        return Interaction(
            lines or lines_square,
            player_obj,
            enemies_list,
            time_limit,
            keyboard_obj,
            frame_obj,
        )

    return factory
