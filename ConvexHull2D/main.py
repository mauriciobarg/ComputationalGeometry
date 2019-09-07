from GeometricEntities import Point
from ConvexHull2D import ConvexHull2D
import pandas as pd
import matplotlib.pyplot as plt


data_nuvem1 = pd.read_csv('ConvexHull2D/nuvem1.txt', sep="   ",
                          header=None, engine='python', names=['x', 'y'])
data_nuvem2 = pd.read_csv('ConvexHull2D/nuvem2.txt', sep="   ",
                          header=None, engine='python', names=['x', 'y'])

points_nuvem1 = []
for i in range(data_nuvem1.shape[0]):
    points_nuvem1.append(Point(data_nuvem1.iloc[i][0], data_nuvem1.iloc[i][1]))

points_nuvem2 = []
for i in range(data_nuvem2.shape[0]):
    points_nuvem2.append(Point(data_nuvem2.iloc[i][0], data_nuvem2.iloc[i][1]))


hull_1 = ConvexHull2D(points_nuvem1)
hull_2 = ConvexHull2D(points_nuvem2)

# with open("fecho1.txt", "w") as fecho1:
#     for p in hull_1:
#         fecho1.write(str(p.getX()) + "   " + str(p.getY()) + "\n")

# with open("fecho2.txt", "w") as fecho2:
#     for p in hull_2:
#         fecho2.write(str(p.getX()) + "   " + str(p.getY()) + "\n")

nuvem_1 = plt.scatter(data_nuvem1['x'], data_nuvem1['y'], c="r")
plt.plot([hull_1[-1].getX(), hull_1[0].getX()], [hull_1[-1].getY(), hull_1[0].getY()], c="black")
for i in range(len(hull_1) - 1):
    plt.plot([hull_1[i].getX(), hull_1[i + 1].getX()], [hull_1[i].getY(), hull_1[i + 1].getY()], c="black")

plt.show()

nuvem_2 = plt.scatter(data_nuvem2['x'], data_nuvem2['y'], c="r")
plt.plot([hull_2[-1].getX(), hull_2[0].getX()], [hull_2[-1].getY(), hull_2[0].getY()], c="black")
for i in range(len(hull_2) - 1):
    plt.plot([hull_2[i].getX(), hull_2[i + 1].getX()], [hull_2[i].getY(), hull_2[i + 1].getY()], c="black")

plt.show()