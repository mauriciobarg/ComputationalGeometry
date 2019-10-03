# from GeometricEntities import Point, Polygon, LineSegment
# from typing import Type, List
# from random import choice


# def DelaunayTriangulation(points: Type[List[Point]]) -> Type[List[Point]]:

def dot(a, b):

    return a.x*b.x + a.y*b.y + a.z*b.z

def cross(a, b):

    return Point( a.y*b.z-a.z*b.y, a.z*b.x-a.x*b.z, a.x*b.y-a.y*b.x )


class Point:

    def __init__(s, x, y, z=0):
        s.x = x
        s.y = y
        s.z = z

    def __repr__(s):

        return "( " + str(s.x) + ", " + str(s.y) + " )"

    def __add__(s, b):

        return Point(s.x+b.x, s.y+b.y)

    def __sub__(s, b):

        return Point(s.x-b.x, s.y-b.y)

    def __mul__(s, b):

        return Point(b*s.x, b*s.y)

    __rmul__ = __mul__

    def IsIn(self, t):
        ''' Checks to see if p is in t using the barycenter method'''
        b = t.v[1] - t.v[0]
        c = t.v[2] - t.v[0]
        d = self   - t.v[0]

        det = c.x*b.y-c.y*b.x;
        u = (d.x*b.y-d.y*b.x)//float(det);
        v = (c.x*d.y-c.y*d.x)//float(det);

        return u >= 0 and v >= 0 and u + v < 1

    def IsInCircumcircleOf(self, T):

        a = T.v[0] - T.v[2]
        b = T.v[1] - T.v[2]

        # Ref: https://en.wikipedia.org/wiki/Circumscribed_circle#Circumcircle_equations
        z = cross(a,b)
        p0 = cross(dot(a,a)*b-dot(b,b)*a, z)*(0.5/dot(z,z)) + T.v[2]

        r2 = 0.25*dot(a, a)*dot(b,b)*dot(a-b, a-b)/dot(z, z)

        return dot(self-p0, self-p0) <= r2

class Triangle:


    def __init__(self, a, b, c):
        
        self.v = [None]*3
        self.v[0] = a
        self.v[1] = b
        self.v[2] = c

        self.neighbour = [None]*3    # Adjacent triangles


    def __repr__(s):

        '''
        return '<%s, [%s, %s, %s]>' % (
                hex(id(s)), 
                hex(id(s.neighbour[0])), 
                hex(id(s.neighbour[1])), 
                hex(id(s.neighbour[2])))
        '''
        return '< ' + str(s.v) + ' >'
        
    def SetEdge(self, edge, T):
        'Set the edge neighbour that matches "edge" to T'

        temp_v = self.v + self.v[0:1]
        for i in range(3):
            if edge[0] == temp_v[i] and edge[1] == temp_v[i+1]:
                self.neighbour[(i+2)%3] = T
                return


class Delaunay_Triangulation:
    """Bowyer Watson"""

    def __init__(self):

        # Create a two triangle 'frame'
        
        a = Point(0, 0)
        b = Point(99, 0)
        c = Point(99, 99)
        d = Point(0, 99)

        T1 = Triangle(a, d, b)
        T2 = Triangle(c, b, d)

        T1.neighbour[0] = T2
        T2.neighbour[0] = T1

        self.triangles = [T1, T2]


    def AddPoint(self, p):
       
        bad_triangles = []

        # Search for the triangle where the point is.
        ''' For now I am just doing a naive search,
        but I hope to replace this with an initial guess
        and a BFS'''
        for T in self.triangles:
            
            if p.IsInCircumcircleOf(T):
                bad_triangles.append(T)


        # Find the convex hull of the bad triangles.
        # Expressed a list of edges (point pairs) in ccw order
        boundary = self.Boundary(bad_triangles)


        for T in bad_triangles:
            self.triangles.remove(T)

        # Retriangle to hole
        new_triangles = []
        for edge in boundary:
            T = Triangle(p, edge[0], edge[1])

            T.neighbour[0] = edge[2]                   # To neighbour
            if T.neighbour[0]:
                T.neighbour[0].SetEdge(edge[1::-1], T)     # from neighbour

            new_triangles.append(T)

        # Link the new triangles
        N = len(new_triangles)
        for i, T in enumerate(new_triangles):
            T.neighbour[2] = new_triangles[(i-1) % N]   # back
            T.neighbour[1] = new_triangles[(i+1) % N]   # forward
   
        self.triangles.extend(new_triangles)

      
    def Boundary(self, bad_triangles):

        # Start with a triangle at random
        T = bad_triangles[0]
        edge = 0

        boundary = []

        while True:
            
            if len(boundary) > 1:
                if boundary[0] == boundary[-1]:
                    break

            if T.neighbour[edge] in bad_triangles:

                last = T
                T = T.neighbour[edge]

                edge = (T.neighbour.index(last) + 1) % 3 

            else:   # Found an edge that is on the boundary
                # Add to list
                boundary.append((T.v[(edge+1)%3], T.v[(edge+2)%3], T.neighbour[edge]))
                edge = (edge + 1) % 3

        return boundary[:-1]

    def export(self):

        ps = [p for t in self.triangles for p in t.v ]

        xs = [p.x for p in ps]
        ys = [p.y for p in ps]
        

        ts = [(ps.index(t.v[0]), ps.index(t.v[1]), ps.index(t.v[2])  ) for t in self.triangles]

        return xs, ys, ts


from random import randint, seed
from math import ceil, sqrt, log, floor


seed(5)
n = 20
xs = [randint(1, 98) for x in range(n)]
ys = [randint(1, 98) for x in range(n)]
zs = [0 for x in range(n)]

DT = Delaunay_Triangulation()
for x, y in zip(xs, ys):
    DT.AddPoint(Point(x, y))

XS, YS, TS = DT.export()


"""
Creating and plotting unstructured triangular grids.
"""
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import math

# Creating a Triangulation without specifying the triangles results in the
# Delaunay triangulation of the points.

# Create the Triangulation; no triangles so Delaunay triangulation created.
triang = tri.Triangulation(xs, ys)

# Plot the triangulation.
fig, ax = plt.subplots()
ax.margins(0.1)
ax.set_aspect('equal')
ax.triplot(triang, 'bo-')

ax.triplot(tri.Triangulation(XS, YS, TS), 'ro--')
ax.set_title('triplot of Delaunay triangulation')


xx = [0, 99, 99, 0] + xs
yy = [0, 0, 99, 99] + ys

tt = [(5,4,0),
(5,0,3),
(8,5,3),
(9,1,0),
(10,2,1),
(13,0,4),
(13,4,9),
(14,9,4),
(14,6,11),
(14,11,12),
(15,9,0),
(15,0,13),
(15,13,9),
(16,3,2),
(16,8,3),
(17,7,5),
(17,5,8),
(17,8,16),
(17,16,7),
(18,4,5),
(18,5,6),
(18,6,14),
(18,14,4),
(19,1,9),
(19,9,14),
(19,14,12),
(19,12,10),
(19,10,1),
(20,16,2),
(20,2,10),
(21,11,10),
(21,10,12),
(21,12,11),
(22,6,16),
(22,16,20),
(22,20,10),
(22,10,11),
(22,11,6),
(23,6,5),
(23,5,7),
(23,7,16),
(23,16,6)]



ax.triplot(tri.Triangulation(xx, yy, tt), 'go--')

plt.show()
