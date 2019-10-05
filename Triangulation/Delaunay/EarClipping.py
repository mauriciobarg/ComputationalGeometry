from GeometricEntities import Point, Polygon, LineSegment, Triangle
from typing import Type, List
from random import choice


def EarClippingTriangulation(polygon: Type[Polygon]) -> Type[List[Point]]:

    vertices = polygon.getVertices()
    sides = polygon.getSides()
    
    triangles = []
    diagonals = []
    while (len(vertices) > 3):

        v = choice(vertices)
        i = vertices.index(v)
        v_last = vertices[i - 1]

        ## If there's an index error, v is the last vertex and the next is the one where it started.
        try:
            v_next = vertices[i + 1]
        except IndexError:
            v_next = vertices[0]
        
        diagonal = LineSegment(v_last, v_next)

        intersection_count = 0
        for side in sides:
            if (diagonal.checkIntersection(side)):
                intersection_count += 1
        
        ## Diagonals must have exactly four intersections with the polygon sides.
        if (intersection_count != 4):
            continue
        else:
            v_last_last = vertices[i - 2]

            v1 = v.getVectorToPoint(v_last)
            v2 = v_last_last.getVectorToPoint(v_last)
            v3 = v_next.getVectorToPoint(v_last)

            crossProducts = [v1.crossProduct(v2), v1.crossProduct(v3), v3.crossProduct(v2)]
            p1 = crossProducts[0]
            p2 = crossProducts[1]
            p3 = crossProducts[2]

            ## This checks if the diagonal is inside or outside the polygon.
            ## https://stackoverflow.com/questions/693806/how-to-determine-whether-v3-is-between-v1-and-v2-when-we-go-from-v1-to-v2-counter/693969#693969
            if ((p1 >= 0 and p2 >= 0 and p3 >= 0) or ((p1 < 0) and not (p2 < 0 and p3 < 0))):
                diagonals.append(diagonal)
                where_to = polygon.findSide(LineSegment(v_last, v))
                sides.pop(polygon.findSide(LineSegment(v_last, v)))
                sides.pop(polygon.findSide(LineSegment(v, v_next)))
                vertices.remove(v)
                triangles.append(Triangle([v, v_next, v_last]))
                sides.insert(where_to, LineSegment(v_last, v_next))

    triangles.append(Triangle(vertices))

    return triangles