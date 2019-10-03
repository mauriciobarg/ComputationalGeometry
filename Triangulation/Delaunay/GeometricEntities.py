from __future__ import annotations
from typing import Type, List, Tuple
from math import sqrt
from MinimumCircle import MinimumCircle


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
        return Point((self._x + p.getX()) / 2, (self._y + p.getY()) / 2)

    def getVectorToPoint(self, p: Type[Point]) -> Type[Vector]:
        return Vector(self._x - p.getX(), self._y - p.getY())

    def isColinear(self, p1: Type[Point], p2: Type[Point]):
        return ((p2.getY() - p1.getY()) * (p1.getX() - self._x) == (p1.getY() - self._y) * (p2.getX() - p1.getX()))

    def findOrientation(self, p1: Type[Point], p2: Type[Point]) -> int:
        px, py = self._x, self._y
        qx, qy = p1.getX(), p1.getY()
        rx, ry = p2.getX(), p2.getY()
        val = ((qy - py) * (rx - qx)) - ((qx - px) * (ry - qy))

        if (val == 0):
            return 0
        return -1 if (val > 0) else 1


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
    
    def crossProduct(self, v: Type[Vector]) -> float:
        (vi, vj) = v.getComponents()
        return self._i * vj - self._j * vi


class LineSegment(object):
    def __init__(self, p1: Type[Point], p2: Type[Point]) -> None:
        self._p1 = p1
        self._p2 = p2

    def getP1(self) -> Type[Point]:
        return self._p1

    def getP2(self) -> Type[Point]:
        return self._p2

    def checkInLine(self, p: Type[Point]) -> bool:
        px, py = p.getX(), p.getY()
        p1x, p1y = self._p1.getX(), self._p1.getY()
        p2x, p2y = self._p2.getX(), self._p2.getY()

        return (px <= max(p1x, p2x) and px <= min(p1x, p2x) and py <= max(p1y, p2y) and py <= min(p1y, p2y))

    def checkIntersection(self, l: Type[LineSegment]):
        l1_p1, l1_p2 = self._p1, self._p2
        l2_p1, l2_p2 = l.getP1(), l.getP2()

        dir_1 = l1_p1.findOrientation(l1_p2, l2_p1)
        dir_2 = l1_p1.findOrientation(l1_p2, l2_p2)
        dir_3 = l2_p1.findOrientation(l2_p2, l1_p1)
        dir_4 = l2_p1.findOrientation(l2_p2, l1_p2)

        if (dir_1 != dir_2 and dir_3 != dir_4):
            return True
        if (dir_1 == 0 and self.checkInLine(l2_p1)):
            return True
        if (dir_2 == 0 and self.checkInLine(l2_p2)):
            return True
        if (dir_3 == 0 and self.checkInLine(l1_p1)):
            return True
        if (dir_4 == 0 and self.checkInLine(l1_p1)):
            return True
        
        return False

class Polygon(object):
    def __init__(self, vertices: Type[List[Point]]) -> None:
        self._vertices = vertices
        self._sides = [LineSegment(vertices[i], vertices[i + 1]) for i in range(len(self._vertices) - 1)]
        self._sides.append(LineSegment(vertices[-1], vertices[0]))
    
    def getSides(self) -> Type[List[LineSegment]]:
        return self._sides

    def getVertices(self) -> Type[List[Point]]:
        return self._vertices

    def findSide(self, l: Type[LineSegment]) -> int:
        for side in self._sides:
            if (side.getP1() == l.getP1() and side.getP2() == l.getP2()):
                return self._sides.index(side)


class Triangle(object):
    def __init__(self, v0: Point, v1: Point, v2: Point) -> None:
        self._v0 = v0
        self._v1 = v1
        self._v2 = v2
        self._neighbors = [None]*3
    
    def getVertices(self) ->  Type[Tuple[Point]]:
        return (self._v0, self._v1, self._v2)

    def isPointInside(self, p: Point) -> bool:
        side1 = p.findOrientation(self._v0, self._v1)
        side2 = p.findOrientation(self._v1, self._v2)
        side3 = p.findOrientation(self._v2, self._v0)
        
        return (side1 == 1) and (side2 == 2) and (side3 == 1)
    
    def isPointInsideCircumcircle(self, p: Point) -> bool:
        circumcircle = MinimumCircle([self._v0, self._v1, self._v2])
        return circumcircle.isPointInside(p)
    
    def setNeighbor(self, t: Type[Triangle], oppositeVertex: int) -> None:
        self._neighbors[oppositeVertex] = t
    

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
        self._center = Point(self._center.getX(
        ) + distance * unit_vector[0], self._center.getY() + distance * unit_vector[1])
