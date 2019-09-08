from GeometricEntities import Point
from PseudoAngle import PseudoAnglePoints
from typing import Type, List


def ConvexHull2D(points_list: Type[List[Point]]) -> Type[List[Point]]:

    starting_point = min(points_list, key=lambda p: (p.getY(), -p.getX()))
    i = points_list.index(starting_point)

    points_list[0], points_list[i] = points_list[i], points_list[0]

    points_list[1:] = sorted(
        points_list[1:],
        key=lambda p: (PseudoAnglePoints(points_list[0], p), points_list[0].distanceToPointSquared(p)))

    ## Removes points that are colinear.
    points_list_no_colinear = points_list[:]
    for i in range(1, len(points_list) - 1):
        if points_list[0].isColinear(points_list[i], points_list[i + 1]):
            points_list_no_colinear.remove(points_list[i])

    points_list = points_list_no_colinear

    if (len(points_list) < 3):
        return "No convex hull exists!"

    convex_hull = []
    convex_hull.extend(points_list[0:3])

    ## Check for orientation change.
    for p in points_list[3:]:
        while (convex_hull[-2].findOrientation(convex_hull[-1], p) == -1):
            convex_hull.pop()
        convex_hull.append(p)

    return convex_hull
