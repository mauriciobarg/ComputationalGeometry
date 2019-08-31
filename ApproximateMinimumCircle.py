from typing import Type, List
from GeometricEntities import Point, Circle

def ApproximateMinimumCircle(points_list: List[Type[Point]]) -> Type[Circle]:
    
    (min_x, max_x) = min(points_list, key=lambda x: x.getX()), max(points_list, key=lambda x: x.getX())
    (min_y, max_y) = min(points_list, key=lambda x: x.getY()), max(points_list, key=lambda x: x.getY())
    possible_pairs = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
    
    max_distance = 0
    starting_pair = None
    
    for pair in possible_pairs:
        distance = pair[0].distanceToPointSquared(pair[1])
        if  (distance > max_distance):
            starting_pair = pair
            max_distance = distance
    
    points_list.remove(starting_pair[0])
    points_list.remove(starting_pair[1])
    
    minimum_circle = Circle(starting_pair[0].middlePointToPoint(starting_pair[1]), 
                            starting_pair[0].distanceToPoint(starting_pair[1]) / 2)
    
    for point in points_list:
        if not (minimum_circle.isPointInside(point)):
            c = minimum_circle.getCenter()
            d = point.distanceToPoint(c)
            minimum_circle.moveCenter((d - minimum_circle.getRadius()) / 2, point.getVectorToPoint(c))
            minimum_circle.varyRadius((d - minimum_circle.getRadius()) / 2)
    
    return minimum_circle
