from Delaunay import DelaunayTriangulation
from GeometricEntities import Point, Polygon
import pandas as pd
import matplotlib.pyplot as plt
from EarClipping import EarClippingTriangulation
from ConvexHull2D import ConvexHull2D

data_nuvem1 = pd.read_csv('nuvem1.txt', sep="   ",
                          header=None, engine='python', names=['x', 'y'])
data_nuvem2 = pd.read_csv('nuvem2.txt', sep="   ",
                          header=None, engine='python', names=['x', 'y'])

points_nuvem1 = []
for i in range(data_nuvem1.shape[0]):
    points_nuvem1.append(Point(data_nuvem1.iloc[i][0], data_nuvem1.iloc[i][1]))

points_nuvem2 = []
for i in range(data_nuvem2.shape[0]):
    points_nuvem2.append(Point(data_nuvem2.iloc[i][0], data_nuvem2.iloc[i][1]))

# dt1 = DelaunayTriangulation(points_nuvem1)
dt2 = DelaunayTriangulation(points_nuvem2)


# nuvem_1 = plt.scatter(data_nuvem1['x'], data_nuvem1['y'], c="r")
# for t in dt1._triangles:
#     for line in t.getSides():
#         plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="black")
# plt.show()

nuvem_2 = plt.scatter(data_nuvem2['x'], data_nuvem2['y'], c="r")
for t in dt2._triangles:
    for line in t.getSides():
        plt.plot([line.getP1().getX(), line.getP2().getX()], [line.getP1().getY(), line.getP2().getY()], c="black")
plt.show()



# with open("delaunay1.txt", "w") as diag1:
#     for t in dt1._triangles:
#         v = t.getVertices()
#         diag1.write(str(points_nuvem1.index(v[0])) + " " + str(points_nuvem1.index(v[1])) + " " + str(points_nuvem1.index(v[2])) + "\n")
#         # diag1.write(str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")

# with open("delaunay2_coords.txt", "w") as diag2:
#     for t in dt2._triangles:
#         v = t.getVertices()
#         #diag2.write(str(points_nuvem2.index(v[0])) + " " + str(points_nuvem2.index(v[1])) + " " + str(points_nuvem2.index(v[2])) + "\n")
#         diag2.write(str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")


