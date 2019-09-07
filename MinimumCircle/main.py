#!/usr/bin/python3
# -*- coding: utf-8 -*-
from GeometricEntities import Point
from ApproximateMinimumCircle import ApproximateMinimumCircle
from MinimumCircle import MinimumCircle
from random import randrange
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import datetime

data = pd.read_csv('MinimumCircle/points.txt', sep="   ",
                   header=None, engine='python', names=['x', 'y'])

points = []
for i in range(data.shape[0]):
    points.append(Point(data.iloc[i][0], data.iloc[i][1]))

approximate_minimum_circle = ApproximateMinimumCircle(points[:])
minimum_circle = MinimumCircle(points[:])

print("Círculo Aproximado: ", approximate_minimum_circle.getCenter(
).getCoordinates(), approximate_minimum_circle.getRadius())
print("Círculo: ", minimum_circle.getCenter(
).getCoordinates(), minimum_circle.getRadius())

approximate_min_circle_plot = plt.Circle(approximate_minimum_circle.getCenter(
).getCoordinates(), radius=approximate_minimum_circle.getRadius(), fill=False, color='r')
min_circle_plot = plt.Circle(minimum_circle.getCenter(
).getCoordinates(), radius=minimum_circle.getRadius(), fill=False)

plt.scatter(data['x'], data['y'])
fig = plt.gcf()
ax = fig.gca()
ax.add_artist(approximate_min_circle_plot)
ax.add_artist(min_circle_plot)
plt.xlim((100, 700))
plt.ylim((100, 500))
ax.set_aspect('equal')
plt.show()


def CompareRunTimes():

    n = []
    run_time_exact = []
    run_time_approximate = []

    for i in range(99, 2001):
        n.append(i)

        random_points = []
        for j in range(i):
            random_points.append(Point(randrange(0, 1000), randrange(0, 1000)))

        start_time = datetime.datetime.now()
        ApproximateMinimumCircle(random_points[:])
        finish_time = datetime.datetime.now()

        run_time_approximate.append((finish_time - start_time).total_seconds())

        start_time = datetime.datetime.now()
        ApproximateMinimumCircle(random_points[:])
        finish_time = datetime.datetime.now()

        run_time_exact.append((finish_time - start_time).total_seconds())

        print("Progress: ", i)

        z1 = numpy.polynomial.polynomial.polyfit(n, run_time_approximate, 1)
        p1 = numpy.poly1d(z1)

        z2 = numpy.polynomial.polynomial.polyfit(n, run_time_exact, 1)
        p2 = numpy.poly1d(z2)

    plt.plot(n, p1(n), "r--")
    plt.plot(n, p2(n), "--")
    plt.show()

# CompareRunTimes()
