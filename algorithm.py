import networkx
import itertools
import math
import numpy
import sys


def distance(a, b):
    return numpy.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def is_between(a, c, b):
    return -sys.float_info.epsilon < (distance(a,c) + distance(c,b)) - distance(a,b) < sys.float_info.epsilon


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
        self.roads_length_factor = 1
        self.paths_length_factor = 1

        self.points = []
        edges = []

        for x, y in point_tuples:
            self.points.append(Point(x, y, Point.TYPE_TOWN))
        max_dist = 0
        for a, b in itertools.combinations(self.points, 2):
            dist = math.sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y, 2))
            if dist >= max_dist:
                max_dist = dist
                town_a = a
                town_b = b

        edges.append((town_a, town_b))
        x = [town_a.x, town_b.x]
        y = [town_a.y, town_b.y]
        coefficients = numpy.polyfit(x, y, 1)
        a1 = coefficients[0]
        b1 = coefficients[1]
        a2 = -(1/a1)
        crossroads = []
        for city in self.points:
            if not(is_between(town_a, city, town_b)):
                b2 = city.y - (city.x * a2)
                x_intersection = (b1 - b2)/(a2 - a1)
                y_intersection = (a2 * b1 - b2 * a1) / (a2 - a1)
                new_crossroad = Point(x_intersection, y_intersection, Point.TYPE_CROSSROAD)
                crossroads.append(new_crossroad)
                edges.append((city, new_crossroad))
        for e1, e2 in edges:
            print(e1, e2)
        self.points += crossroads
        for p in self.points:
            print(p)
        self.state = State(edges)

    def fitness_function(self, state):
        graph = networkx.Graph()

        for edge in state.edges:
            graph.add_edge(edge[0], edge[1], {'weight': distance(edge[0], edge[1])})

        towns = [point for point in self.points if point.type == Point.TYPE_TOWN]

        paths_length = 0
        for i in range(0, len(towns)):
            for j in range(i + 1, len(towns)):
                paths_length += networkx.shortest_path_length(graph, source=towns[i], target=towns[j], weight='weight')

        roads_length = sum([data['weight'] for node_a, node_b, data in graph.edges(data=True)])

        return self.roads_length_factor * roads_length + self.paths_length_factor * paths_length
