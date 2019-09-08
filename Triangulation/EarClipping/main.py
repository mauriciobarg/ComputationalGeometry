from GeometricEntities import Point, Polygon, LineSegment
from typing import Type, List
from PseudoAngle import PseudoAnglePoints
from random import choice
from copy import deepcopy
import pandas as pd
import matplotlib.pyplot as plt

data_polygon1 = pd.read_csv('Triangulation/EarClipping/polygon1.txt', sep="   ",
                          header=None, engine='python', names=['x', 'y'])

data_polygon2 = pd.read_csv('Triangulation/EarClipping/polygon2.txt', sep="   ",
                          header=None, engine='python', names=['x', 'y'])


points_polygon1 = []
for i in range(data_polygon1.shape[0]):
    points_polygon1.append(Point(data_polygon1.iloc[i][0], data_polygon1.iloc[i][1]))

points_polygon2 = []
for i in range(data_polygon2.shape[0]):
    points_polygon2.append(Point(data_polygon2.iloc[i][0], data_polygon2.iloc[i][1]))

poly1 = Polygon(points_polygon1)
poly2 = Polygon(points_polygon2)

def EarClippingTriangulation(polygon: Type[Polygon]) -> Type[List[Point]]:

    vertices = polygon.getVertices()
    sides = polygon.getSides()

    diagonals = []
    while (len(vertices) > 3):

        plt.scatter([p.getX() for p in polygon.getVertices()], [p.getY() for p in polygon.getVertices()], c="r")
        for line in polygon.getSides():
            plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="black")

        v = choice(vertices)
        i = vertices.index(v)
        v_last = vertices[i - 1]
        try:
            v_next = vertices[i + 1]
        except IndexError:
            v_next = vertices[0]
        
        diagonal = LineSegment(v_last, v_next)

        plt.plot([v_last.getX(), v_next.getX()], [v_last.getY(), v_next.getY()], c="red")


        intersection_count = 0
        for side in sides:
            if (diagonal.checkIntersection(side)):
                intersection_count += 1
        
        if (intersection_count != 4):
            continue
        else:
            v_last_last = vertices[i - 2]
            if PseudoAnglePoints(v, v_last) < PseudoAnglePoints(v_next, v_last) < PseudoAnglePoints(v_last_last, v_last):
                diagonals.append(diagonal)
                where_to = polygon.findSide(LineSegment(v_last, v))
                sides.pop(polygon.findSide(LineSegment(v_last, v)))
                sides.pop(polygon.findSide(LineSegment(v, v_next)))
                vertices.remove(v)
                sides.insert(where_to, LineSegment(v_last, v_next))

            # for line in diagonals:
            #     plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="blue")
        
        plt.show()
    return diagonals


# diags1 = EarClippingTriangulation(deepcopy(poly1))
# plt.scatter([p.getX() for p in poly1.getVertices()], [p.getY() for p in poly1.getVertices()], c="r")
# for line in poly1.getSides():
#     plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="black")

# for line in diags1:
#     plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="blue")

# plt.show()

diags2 = EarClippingTriangulation(deepcopy(poly2))
plt.scatter([p.getX() for p in poly2.getVertices()], [p.getY() for p in poly2.getVertices()], c="r")
for line in poly2.getSides():
    plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="black")

for line in diags2:
    plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="blue")

plt.show()
