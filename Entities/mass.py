from Entities.ball import Ball
from Game_Control.Vector import Vector
from SimpleGUICS2Pygame.simpleguics2pygame import Canvas


class Mass(Ball):
    """Mass is ejected from player and enemy objects when the velocity is changed directly.
    This is not ejected due to bounce or other external forces.
    When the object itself chooses to change directions, then mass is ejected making the original ball smaller.
    Mass is sub-class of Ball which means that it inherits the functionalities such as movement and bounce.
    """

    def __init__(self, position: Vector, velocity: Vector, radius: int) -> None:
        """Initializes Mass object.
        Mass will have the same functionality of Ball but will have some extra.

        Args:
            Mass: super-class of Player.
        """
        super().__init__(position, velocity, 2)  # Use the initializer from super-class
        self.type: str = "Mass"
        self.colour: str = "Aqua"
        self.radius: int = radius

    def draw(self, canvas: Canvas) -> None:
        """Draws ball and ball center.
        Draws circles to represent ball, it takes the initial position, radius (hardcoded) and colour.
        Draws point which represents center of the circle for easier computation later. It takes initial position and colour as argument.
        Initial position is given as Vector type for computation. Vector is converted to tuple.

        Args:
            canvas: where the game play takes place.
        """
        canvas.draw_circle(
            self.position.get_p(), 2, 1, self.colour, self.colour
        )  # Draws ball as circle
        canvas.draw_point(
            self.position.get_p(), self.colour
        )  # Draws point as the center of the ball
