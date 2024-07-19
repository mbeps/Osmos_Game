from Game_Control.Vector import Vector
from SimpleGUICS2Pygame.simpleguics2pygame import Canvas
from Entities.ball import Ball


class Line:
    """Walls are where ball objects bounce against.
    When a ball object collides with wall, the ball object will bounce.
    Normal of the wall is needed to make the ball bounce.
    """

    def __init__(self, point1: Vector, point2: Vector) -> None:
        """Initializes wall object for drawing and managing wall.
        Normal is worked out bt computing line parallel to the wall and finding the perpendicular.

        Args:
            point1: point from which the wall is drawn
            point2: point to where the line is drawn
        """
        self.point_a: Vector = point1
        self.point_b: Vector = point2
        self.unit: Vector = self.point_b.copy().subtract(self.point_a).normalize()
        self.normal: Vector = self.unit.copy().rotate_anti()
        self.thickness: int = 30

    def draw(self, canvas: Canvas) -> None:
        """Draws line as wall.
        Takes start point and end point as argument to draw the line between given point. Thickess and colour are also added.

        Args:
            canvas: where the game play takes place
        """
        canvas.draw_line(
            self.point_a.get_p(), self.point_b.get_p(), self.thickness, "white"
        )

    def distance_vector(self, position: Vector) -> Vector:
        """Uses shortest distance from center of ball to wall as Vector object
        Distance is computed and line projected.

        Args:
            position: current position of the ball

        Returns:
            projection of the line between ball and wall
        """
        position_to_a: Vector = position.copy().subtract(
            self.point_a
        )  # Shortest distance between ball and wall as vector
        return position_to_a.get_proj(self.normal)  # Modulus of the distance

    def distance(self, ball: Ball) -> float:
        """Works out distance of the ball from ball as integer.

        Args:
            ball: ball object

        Returns:
            distance from ball to wall

        Calls:
            distance used to fetch the distance from ball in vector form
        """
        return self.distance_vector(
            ball.position
        ).length()  # Shortest distance between ball and wall as length
