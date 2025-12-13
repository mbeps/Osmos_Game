from __future__ import annotations

import types
from collections.abc import Callable
from typing import TYPE_CHECKING, TypeAlias

import pytest

import Game_Control.interactions as interactions
from Game_Control.Vector import Vector

if TYPE_CHECKING:
    from Game_Control.interactions import Interaction
    from Maps.line import Line

CanvasArg: TypeAlias = int | float | str | tuple[int, int] | tuple[float, float] | Vector
CanvasCall: TypeAlias = tuple[str, tuple[CanvasArg, ...]]


class DummyTimer:
    def __init__(self, interval: int, handler: Callable[[], None]) -> None:
        self.interval: int = interval
        self.handler: Callable[[], None] = handler
        self.started: bool = False
        self.stop_calls: int = 0

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False
        self.stop_calls += 1

    def trigger(self) -> None:
        self.handler()


class DummyFrame:
    def __init__(self) -> None:
        self.stopped: bool = False

    def stop(self) -> None:
        self.stopped = True


class DummyCanvas:
    def __init__(self) -> None:
        self.calls: list[CanvasCall] = []

    def draw_circle(self, *args: CanvasArg) -> None:
        self.calls.append(("circle", args))

    def draw_point(self, *args: CanvasArg) -> None:
        self.calls.append(("point", args))

    def draw_text(self, *args: CanvasArg) -> None:
        self.calls.append(("text", args))

    def draw_line(self, *args: CanvasArg) -> None:
        self.calls.append(("line", args))


@pytest.fixture
def dummy_canvas() -> DummyCanvas:
    return DummyCanvas()


@pytest.fixture
def simplegui_stub(monkeypatch: pytest.MonkeyPatch) -> types.SimpleNamespace:
    timers: list[DummyTimer] = []
    sg: types.SimpleNamespace = types.SimpleNamespace()

    def create_timer(interval: int, handler: Callable[[], None]) -> DummyTimer:
        timer: DummyTimer = DummyTimer(interval, handler)
        timers.append(timer)
        return timer

    sg.create_timer = create_timer
    sg.timers = timers
    monkeypatch.setattr(interactions, "simplegui", sg)
    return sg


@pytest.fixture
def frame_stub() -> DummyFrame:
    return DummyFrame()


@pytest.fixture
def lines_square() -> list[Line]:
    from Game_Control.Vector import Vector
    from Maps.line import Line

    width: int = 100
    height: int = 80
    return [
        Line(Vector(0, 0), Vector(width, 0)),
        Line(Vector(width, 0), Vector(width, height)),
        Line(Vector(0, height), Vector(width, height)),
        Line(Vector(0, 0), Vector(0, height)),
    ]


@pytest.fixture
def interaction_factory(
    simplegui_stub: types.SimpleNamespace,
    frame_stub: DummyFrame,
    lines_square: list[Line],
) -> Callable[..., Interaction]:
    from Entities.enemy import Enemy
    from Entities.player import Player
    from Game_Control.interactions import Interaction
    from Game_Control.keyboard import Keyboard
    from Game_Control.Vector import Vector
    from Maps.line import Line

    def factory(
        player: Player | None = None,
        enemies: list[Enemy] | None = None,
        time_limit: int = 10,
        keyboard: Keyboard | None = None,
        lines: list[Line] | None = None,
        frame: DummyFrame | None = None,
    ) -> Interaction:
        player_obj: Player = player or Player(Vector(10, 10), Vector(0, 0), 20)
        enemies_list: list[Enemy] = enemies or [Enemy(Vector(30, 30), Vector(1, 0), 5)]
        keyboard_obj: Keyboard = keyboard or Keyboard()
        frame_obj: DummyFrame = frame or frame_stub
        return Interaction(
            lines or lines_square,
            player_obj,
            enemies_list,
            time_limit,
            keyboard_obj,
            frame_obj,
        )

    return factory
