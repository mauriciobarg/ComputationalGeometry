from __future__ import annotations
from typing import Type, List
from math import sqrt

class Point(object):
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def getX(self) -> float:
        return self._x

    def getY(self) -> float:
        return self._y
    
    def getCoordinates(self) -> (float, float):
        return (self._x, self._y)
    
    def setCoordinates(self, x: float, y: float) -> None:
        self._x = x
        self._y = y
        
    def distanceToPoint(self, p: Type[Point]) -> float:
        return sqrt((self._x - p.getX())**2 + (self._y - p.getY())**2)
    
    def distanceToPointSquared(self, p: Type[Point]) -> float:
        return (self._x - p.getX())**2 + (self._y - p.getY())**2
    
    def middlePointToPoint(self, p: Type[Point]) -> Type[Point]:
        return Point((self._x + p.getX()) / 2, (self._y  + p.getY()) / 2)
    
    def getVectorToPoint(self, p: Type[Point]) -> Type[Vector]:
        return Vector(self._x - p.getX(), self._y - p.getY())
    
    def isColinear(self, p1: Type[Point], p2: Type[Point]):
        return ((p2.getY() - p1.getY()) * (p1.getX() - self._x) == (p1.getY() - self._y) * (p2.getX() - p1.getX())) 
        
class Vector(object):
    def __init__(self, i: float, j: float) -> None:
        self._i = i
        self._j = j

    def getModulus(self) -> float:
        return sqrt(self._i**2 + self._j**2)

    def getUnitVector(self) -> Type[Vector]:
        m = self.getModulus()
        return Vector(self._i / m, self._j / m)
    
    def getComponents(self):
        return (self._i, self._j)


class Circle(object):
    def __init__(self, center: Type[Point], radius: float) -> None:
        self._center = center
        self._radius = radius
    
    def setCenter(self, c: Point) -> None:
        self._center = c
    
    def setRadius(self, r: float) -> float:
        self._radius = r
    
    def varyRadius(self, v: float) -> None:
        self._radius += v
    
    def getRadius(self) -> float:
        return self._radius
    
    def getCenter(self) -> Type[Point]:
        return self._center

    def isPointInside(self, p: Type[Point]) -> bool:
        return p.distanceToPointSquared(self._center) <= self._radius**2

    def moveCenter(self, distance: float, direction: Type[Vector]) -> None:
        unit_vector = direction.getUnitVector().getComponents()
        self._center = Point(self._center.getX() + distance * unit_vector[0], self._center.getY() + distance * unit_vector[1])