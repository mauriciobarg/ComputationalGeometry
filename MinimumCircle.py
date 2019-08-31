from GeometricEntities import Point, Circle
from typing import Type, List
from random import shuffle

def MinimumCircle(points_list: List[Type[Point]], other_points: List[Type[Point]] = []) -> Type[Circle]:
    if len(other_points) > 2:
        return None
    else:
        shuffle(points_list)
        points_list.extend(other_points)

    if (len(points_list) == 0):
        return None

    elif (len(points_list) == 1):
        return Circle(points_list[0], 0)

    elif (len(points_list) == 2):
        return Circle(points_list[0].middlePointToPoint(points_list[1]), points_list[0].distanceToPoint(points_list[1]) / 2)

    elif (len(points_list) == 3):
        triangle_vertices = [(points_list[0], points_list[1]), (points_list[0], points_list[2]), (points_list[1], points_list[2])]
        triangle_sides = sorted(triangle_vertices, key=lambda x: x[0].distanceToPointSquared(x[1]))
        circle_points = max(triangle_vertices, key=lambda x: x[0].distanceToPointSquared(x[1]))
        
        if (points_list[0].isColinear(points_list[1], points_list[2])):
            return Circle(circle_points[0].middlePointToPoint(circle_points[1]), circle_points[0].distanceToPoint(circle_points[1]) / 2)
        
        else:
            side_a = triangle_sides[0][0].distanceToPointSquared(triangle_sides[0][1])
            side_b = triangle_sides[1][0].distanceToPointSquared(triangle_sides[1][1])
            side_c = triangle_sides[2][0].distanceToPointSquared(triangle_sides[2][1])
            
            if (side_a > side_b + side_c):
                return Circle(circle_points[0].middlePointToPoint(circle_points[1]), circle_points[0].distanceToPoint(circle_points[1]) / 2)
            
            else:
                ax = points_list[0].getX()
                ay = points_list[0].getY()
                bx = points_list[1].getX()
                by = points_list[1].getY()
                cx = points_list[2].getX()
                cy = points_list[2].getY()
                d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
                ux = (1 / d) * ((ax**2 + ay**2)*(by - cy) + (bx**2 + by**2)*(cy - ay) + (cx**2 + cy**2)*(ay - by))
                uy = (1 / d) * ((ax**2 + ay**2)*(cx - bx) + (bx**2 + by**2)*(ax - cx) + (cx**2 + cy**2)*(bx - ax))
                center = Point(ux, uy)

                return Circle(center, center.distanceToPoint(points_list[0]))

    else:
        minimum_circle = None
        if (len(other_points) == 0):
            point_p1 = points_list[0]
            point_p2 = points_list[1]
            minimum_circle = MinimumCircle([point_p1, point_p2])

            for i, p in enumerate(points_list[2:]):
                if minimum_circle != None:
                    if not (minimum_circle.isPointInside(p)):
                        minimum_circle = MinimumCircle(points_list[:i + 2], [p])
                else:
                    minimum_circle = MinimumCircle(points_list[:i + 2], [p])

            return minimum_circle

        elif (len(other_points) == 1):
            point_q1 = points_list.pop()
            point_p1 = points_list[0]
            minimum_circle = MinimumCircle([point_p1, point_q1])
            
            for i, p in enumerate(points_list[1:]):
                if minimum_circle != None:
                    if not (minimum_circle.isPointInside(p)):
                        minimum_circle = MinimumCircle(points_list[:i + 1], [p, point_q1])
                else:
                    minimum_circle = MinimumCircle(points_list[:i + 1], [p, point_q1])
            return minimum_circle

        elif (len(other_points) == 2):
            point_q2 = points_list.pop()
            point_q1 = points_list.pop()
            minimum_circle = MinimumCircle([point_q1, point_q2])
            for p in points_list:
                if minimum_circle != None:
                    if not (minimum_circle.isPointInside(p)):
                        minimum_circle = MinimumCircle([p, point_q1, point_q2])
                else:
                    minimum_circle = MinimumCircle([p, point_q1, point_q2])

            return minimum_circle