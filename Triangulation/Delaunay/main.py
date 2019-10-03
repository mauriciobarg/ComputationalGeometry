from GeometricEntities import Point, Polygon
from EarClipping import EarClippingTriangulation
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

diags1 = EarClippingTriangulation(deepcopy(poly1))
diags2 = EarClippingTriangulation(deepcopy(poly2))

# with open("diagonals1.txt", "w") as diag1:
#     for line in diags1:
#         diag1.write(str(line.getP1().getX()) + "   " + str(line.getP1().getY()) + "   " + str(line.getP2().getX()) + "   " + str(line.getP2().getY()) + "\n")

# with open("diagonals2.txt", "w") as diag2:
#     for line in diags2:
#         diag2.write(str(line.getP1().getX()) + "   " + str(line.getP1().getY()) + "   " + str(line.getP2().getX()) + "   " + str(line.getP2().getY()) + "\n")

plt.scatter([p.getX() for p in poly1.getVertices()], [p.getY() for p in poly1.getVertices()], c="r")
for line in poly1.getSides():
    plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="black")

for line in diags1:
    plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="blue")

plt.show()

plt.scatter([p.getX() for p in poly2.getVertices()], [p.getY() for p in poly2.getVertices()], c="r")
for line in poly2.getSides():
    plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="black")

for line in diags2:
    plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="blue")

plt.show()
