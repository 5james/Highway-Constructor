import itertools
import math
import numpy
import sys

def distance(a,b):
    return numpy.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def is_between(a,c,b):
    return  -sys.float_info.epsilon < (distance(a,c) + distance(c,b)) - distance(a,b) < sys.float_info.epsilon

class Point:
    TYPE_TOWN, TYPE_CROSSROAD = range(0, 2)

    def __init__(self, x, y, point_type):
        self.x = x
        self.y = y
        self.type = point_type

    def __str__(self):
        str = ""
        if self.type == self.TYPE_TOWN:
            str += "Town: "
        else:
            str += "Crossroad: "
        str += repr(self.x) + ", " + repr(self.y)
        return str


class State:
    def __init__(self, edges):
        self.edges = edges


class Algorithm:

    def __init__(self, point_tuples):
        self.points = []
        edges = []

        for x,y in point_tuples:
            self.points.append(Point(x,y,Point.TYPE_TOWN))
        maxDist = 0
        for a, b in itertools.combinations(self.points, 2):
            dist = math.sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y,2))
            if dist >= maxDist:
                maxDist = dist
                townA = a
                townB = b

        edges.append((townA, townB))
        x = [townA.x, townB.x]
        y = [townA.y, townB.y]
        coefficients = numpy.polyfit(x, y, 1)
        a1 = coefficients[0]
        b1 = coefficients[1]
        a2 = -(1/a1)
        crossroads = []
        for city in self.points:
            if not(is_between(townA, city, townB)):
                b2 = city.y - (city.x * a2)
                x_intersection = (b1 - b2)/(a2 - a1)
                y_intersection = (a2 * b1 - b2 * a1) / (a2 - a1)
                new_crossroad = Point(x_intersection, y_intersection, Point.TYPE_CROSSROAD)
                crossroads.append(new_crossroad)
                edges.append((city, new_crossroad))
        for e1,e2 in edges:
            print(e1, e2)
        self.points += crossroads
        for p in self.points:
            print(p)
        self.state = State(edges)