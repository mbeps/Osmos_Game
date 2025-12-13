from __future__ import annotations

import math
from types import NotImplementedType


# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x: float = x
        self.y: float = y

    # Returns a string representation of the vector
    def __str__(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other: Vector | str | int | float | None) -> bool | NotImplementedType:  # type: ignore[override]
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other: Vector | str | int | float | None) -> bool:  # type: ignore[override]
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self) -> tuple[float, float]:
        return (self.x, self.y)  # Tuple representation is used by the canvas

    # Returns a copy of the vector
    def copy(self) -> "Vector":
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other: "Vector") -> "Vector":
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other: "Vector") -> "Vector":
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self) -> "Vector":
        return self.multiply(-1)

    def __neg__(self) -> "Vector":
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other: "Vector") -> "Vector":
        return self.add(-other)

    def __sub__(self, other: "Vector") -> "Vector":
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k: float) -> "Vector":
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k: float) -> "Vector":
        return self.copy().multiply(k)

    def __rmul__(self, k: float) -> "Vector":
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k: float) -> "Vector":
        return self.multiply(1 / k)

    def __truediv__(self, k: float) -> "Vector":
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self) -> "Vector":
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self) -> "Vector":
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other: "Vector") -> float:
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self) -> float:
        return float(self.x**2 + self.y**2)

    # Reflect this vector on a normal
    def reflect(self, normal: "Vector") -> "Vector":
        n = normal.copy()
        n.multiply(2 * self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other: "Vector") -> float:
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self) -> "Vector":
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta: float) -> "Vector":
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta: float) -> "Vector":
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec: "Vector") -> "Vector":
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))
        
        
