from GeometricEntities import Point, Triangle, LineSegment, Polygon
from typing import Type, List
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
from ConvexHull2D import ConvexHull2D
from EarClipping import EarClippingTriangulation

class DelaunayTriangulation(object):
    def __init__(self, points: Type[List[Point]]) -> None:
        self._points = points
        self._triangles = []

        ch = ConvexHull2D(self._points)
        tri = EarClippingTriangulation(Polygon(ch))

        for t in tri:
            self._triangles.append(t)
        
        for i in range(len(self._triangles)):
            for j in range(len(self._triangles)):
                if i != j:
                    self._triangles[i].setNeighbor(self._triangles[j])

        self._super_triangles = []
        for t in self._triangles:
            for v in t.getVertices():
                if v not in self._super_triangles:
                    self._super_triangles.append(v)

        self._points = [p for p in points if p not in self._super_triangles]

        for p in self._points:
            self.addPoint(p)

    def addPoint(self, p: Type[Point]) -> None:

        bad_triangles = []

        for t in self._triangles:
            if t.isPointInsideCircumcircle(p):
                bad_triangles.append(t)

        boundary = self.getBoundary(bad_triangles)

        for t in bad_triangles:
            self._triangles.remove(t)

        new_triangles = []
        for (edge, op_t) in boundary:
            plt.scatter(p.getX(), p.getY(), c='r')

            t = Triangle([p, edge.getP1(), edge.getP2()])

            t.setNeighbor(op_t)
            if op_t:
                t.getNeighbor()[t.getNeighbor().index(op_t)].setNeighbor(t)

            new_triangles.append(t)

        n = len(new_triangles)
        for i, t in enumerate(new_triangles):
            t.setNeighbor(new_triangles[(i + 1) % n])
            t.setNeighbor(new_triangles[(i - 1) % n])
            self._triangles.append(t)

        
    def getBoundary(self, bad_triangles: Type[List[Triangle]]):

        boundary = []
        t = bad_triangles[0]
        t_edges = t.getSides()
        edge = t_edges[0]

        while True:

            op_t = t.getNeighbor(t_edges.index(edge))

            if op_t not in bad_triangles:
                boundary.append((edge, op_t))
                edge = t_edges[(t_edges.index(edge) + 1) % 3]

                if boundary[0][0].getP1() == boundary[-1][0].getP2():
                    break
            
            else:
                old = t
                t = op_t
                t_edges = t.getSides()
                edge = t_edges[(t.getNeighbor().index(old) + 1) % 3]
     
        return boundary

