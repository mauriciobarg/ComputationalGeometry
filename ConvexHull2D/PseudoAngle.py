from __future__ import annotations
from typing import Type
from GeometricEntities import Point, Vector


def PseudoAnglePoints(p1: Type[Point], p2: Type[Point]) -> float:
    (i, j) = p2.getVectorToPoint(p1).getComponents()
    (abs_i, abs_j) = abs(i), abs(j)
    if i == j == 0:
        return 0
    if j > 0:
        if i > 0:
            if abs_i >= abs_j:
                return abs_j / abs_i
            else:
                return 2 - abs_i / abs_j
        else:
            if abs_j >= abs_i:
                return 2 + abs_i / abs_j
            else:
                return 4 - abs_j / abs_i
    else:
        if i < 0:
            if abs_i > abs_j:
                return 4 + abs_j / abs_i
            else:
                return 6 - abs_i / abs_j
        else:
            if abs_j > abs_i:
                return 6 + abs_i / abs_j
            else:
                return 8 - abs_j / abs_i


def PseudoAngleVector(v: Type[Vector]) -> float:
    (i, j) = v.getComponents()
    (abs_i, abs_j) = abs(i), abs(j)
    if i == j == 0:
        return 0
    if j > 0:
        if i > 0:
            if abs_i >= abs_j:
                return abs_j / abs_i
            else:
                return 2 - abs_i / abs_j
        else:
            if abs_j >= abs_i:
                return 2 + abs_i / abs_j
            else:
                return 4 - abs_j / abs_i
    else:
        if i < 0:
            if abs_i > abs_j:
                return 4 + abs_j / abs_i
            else:
                return 6 - abs_i / abs_j
        else:
            if abs_j > abs_i:
                return 6 + abs_i / abs_j
            else:
                return 8 - abs_j / abs_i
