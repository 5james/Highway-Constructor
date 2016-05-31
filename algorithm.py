import networkx
import itertools
import math
import numpy
import sys


def distance(a, b):
    return numpy.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def is_between(a, c, b):
    return -sys.float_info.epsilon < (distance(a, c) + distance(c, b)) - distance(a, b) < sys.float_info.epsilon


class Point:
    TYPE_TOWN, TYPE_CROSSROAD = range(0, 2)

    def __init__(self, x, y, point_type=TYPE_TOWN):
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
        self.points = {edge[0] for edge in self.edges} | {edge[1] for edge in self.edges}

    def get_neighbours(self):
        neighbours = []

        for i in range(0, len(self.points)):
            for j in range(i + 1, len(self.points)):
                # If edge between points[i] and points[j] exist try to delete it, else create it.
                if (self.points[i], self.points[j]) in self.edges or (self.points[j], self.points[i]) in self.edges:
                    # Delete one edge.
                    neighbour_edges = [edge for edge in self.edges
                                 if (edge != (self.points[i], self.points[j])) and (edge != (self.points[j], self.points[i]))]

                    # Check if graph is still connected.
                    graph = networkx.Graph()
                    for edge in neighbour_edges:
                        graph.add_edge(*edge)
                    if graph.is_connected():
                        neighbours.append(State(neighbour_edges))
                else:
                    new_edges = self._sanitize_edges([(self.points[i], self.points[j])])

        return neighbours

    def _sanitize_edges(self, edges):
        """
        Checks if there are points that lay on the edges.
        """
        new_edges = set()
        for edge in edges:
            found_point_between = False
            for point in self.points:
                if point is not edge[0] and point is not edge[1]:
                    if is_between(edge[0], point, edge[1]):
                        if (edge[0], point) not in self.edges and (point, edge[0]) not in self.edges:
                            new_edges.add((edge[0], point))
                        if (edge[1], point) not in self.edges and (point, edge[1]) not in self.edges:
                            new_edges.add((point, edge[1]))
                        found_point_between = True
                        break
            if not found_point_between:
                new_edges.add(edge)

        if set(edges) == new_edges:
            return edges
        else:
            return self._sanitize_edges(list(new_edges))


class Algorithm:

    def __init__(self, point_tuples):
        self.roads_length_factor = 1
        self.paths_length_factor = 1

        self.points = []
        edges = []

        for x, y in point_tuples:
            self.points.append(Point(x, y, Point.TYPE_TOWN))
        max_dist = 0
        for city1, b in itertools.combinations(self.points, 2):
            dist = math.sqrt(pow(b.x-city1.x, 2) + pow(b.y-city1.y, 2))
            if dist >= max_dist:
                max_dist = dist
                town_a = city1
                town_b = b
        if not((town_a.x - town_b.x) == 0) and not((town_a.y -town_b.y) == 0):
            skipped_towns = []

            x = [town_a.x, town_b.x]
            y = [town_a.y, town_b.y]
            coefficients = numpy.polyfit(x, y, 1)
            a1 = coefficients[0]
            b1 = coefficients[1]
            if a1 == 0:
                a2 = 0
            else:
                a2 = -(1/a1)
            crossroads = []
            b_pack = []
            for city in self.points:
                if not (is_between(town_a, city, town_b)):
                    b_pack.append((city.y - (city.x * a2), city))
            b_pack.sort(key=lambda point:point[0])
            collinear_set = set([])
            for i in range(1, len(b_pack)):
                if abs(b_pack[i-1][0] - b_pack[i][0]) < 10*sys.float_info.epsilon:
                    rounded_b_pack = round(b_pack[i][0], 2)
                    collinear_set.add(rounded_b_pack)
            for i in collinear_set:
                collinear = []
                for j in b_pack:
                    if abs(i - j[0]) < sys.float_info.epsilon*100:
                        collinear.append(j[1])
                collinear.sort(key=lambda point:point.x)
                collinear_lower = []
                collinear_higher = []
                for c in collinear:
                    if a1 > 0 and c.y > a1 * c.x + b1:
                        collinear_lower.append(c)
                    else:
                        collinear_higher.append(c)

                for c in range(1, len(collinear_lower)):
                    edges.append((collinear_lower[c-1], collinear_lower[c]))
                    skipped_towns.append(collinear_lower[c-1])
                    self.points.remove(collinear_lower[c-1])

                for c in range(len(collinear_higher)-1, 0, -1):
                    edges.append((collinear_higher[c], collinear_higher[c-1]))
                    skipped_towns.append(collinear_higher[c])
                    self.points.remove(collinear_higher[c])

                collinear_crossroad = Point((b1 - i) / (a2 - a1), (a2 * b1 - i * a1) / (a2 - a1), Point.TYPE_CROSSROAD)
                crossroads.append(collinear_crossroad)
                if not(len(collinear_lower) == 0):
                    edges.append((collinear_lower[len(collinear_lower)-1], collinear_crossroad))
                    skipped_towns.append(collinear_lower[len(collinear_lower)-1])
                    self.points.remove(collinear_lower[len(collinear_lower)-1])
                if not(len(collinear_higher) == 0):
                    edges.append((collinear_higher[0], collinear_crossroad))
                    skipped_towns.append(collinear_higher[0])
                    self.points.remove(collinear_higher[0])

            for city in self.points:
                if not(is_between(town_a, city, town_b)):
                    b2 = city.y - (city.x * a2)
                    if (a2-a1) == 0:
                        x_intersection = city.x
                        y_intersection = town_a.y
                    else:
                        x_intersection = (b1 - b2)/(a2 - a1)
                        y_intersection = (a2 * b1 - b2 * a1) / (a2 - a1)
                    new_crossroad = Point(x_intersection, y_intersection, Point.TYPE_CROSSROAD)
                    for pp in self.points:
                        if (-sys.float_info.epsilon < pp.x -  x_intersection < sys.float_info.epsilon
                            and -sys.float_info.epsilon < pp.y -  y_intersection < sys.float_info.epsilon):
                            new_crossroad = pp
                    crossroads.append(new_crossroad)
                    edges.append((city, new_crossroad))
            self.points += skipped_towns
        elif town_a.x - town_b.x == 0:
            crossroads = []
            skipped_towns = []
            y_pack = []
            y_set = set([])
            for city in self.points:
                y_pack.append(city.y)
            y_pack.sort()
            for i in range(1, len(y_pack)):
                if abs(y_pack[i] - y_pack[i-1]) < sys.float_info.epsilon:
                    y_set.add(y_pack[i])

            for s in y_set:
                collinear_lower = []
                collinear_higher = []
                collinear = []
                for c in self.points:
                    if c.y == s:
                        collinear.append(c)
                for c in collinear:
                    if c.x < town_a.x:
                        collinear_lower.append(c)
                    elif c.x > town_a.x:
                        collinear_higher.append(c)

                for c in range(1, len(collinear_lower)):
                    edges.append((collinear_lower[c-1], collinear_lower[c]))
                    skipped_towns.append(collinear_lower[c-1])
                    self.points.remove(collinear_lower[c-1])

                for c in range(len(collinear_higher)-1, 0, -1):
                    edges.append((collinear_higher[c], collinear_higher[c-1]))
                    skipped_towns.append(collinear_higher[c])
                    self.points.remove(collinear_higher[c])

                collinear_crossroad = Point(town_a.x, s, Point.TYPE_CROSSROAD)
                crossroads.append(collinear_crossroad)
                if not (len(collinear_lower) == 0):
                    edges.append((collinear_lower[len(collinear_lower) - 1], collinear_crossroad))
                    skipped_towns.append(collinear_lower[len(collinear_lower) - 1])
                    self.points.remove(collinear_lower[len(collinear_lower) - 1])
                if not (len(collinear_higher) == 0):
                    edges.append((collinear_higher[0], collinear_crossroad))
                    skipped_towns.append(collinear_higher[0])
                    self.points.remove(collinear_higher[0])

            for city in self.points:
                if not(is_between(town_a, city, town_b)):
                    new_crossroad = Point(town_a.x, city.y, Point.TYPE_CROSSROAD)
                    crossroads.append(new_crossroad)
                    edges.append((city, new_crossroad))
            self.points += skipped_towns
        else:
            crossroads = []
            skipped_towns = []
            x_pack = []
            x_set = set([])
            for city in self.points:
                x_pack.append(city.x)
            x_pack.sort()
            for i in range(1, len(x_pack)):
                if abs(x_pack[i] - x_pack[i-1]) < sys.float_info.epsilon:
                    x_set.add(x_pack[i])
            for s in x_set:
                collinear_lower = []
                collinear_higher = []
                collinear = []
                for c in self.points:
                    if c.x == s:
                        collinear.append(c)
                for c in collinear:
                    if c.y < town_a.y:
                        collinear_lower.append(c)
                    elif c.y > town_a.y:
                        collinear_higher.append(c)

                for c in range(1, len(collinear_lower)):
                    edges.append((collinear_lower[c-1], collinear_lower[c]))
                    skipped_towns.append(collinear_lower[c-1])
                    self.points.remove(collinear_lower[c-1])

                for c in range(len(collinear_higher)-1, 0, -1):
                    edges.append((collinear_higher[c], collinear_higher[c-1]))
                    skipped_towns.append(collinear_higher[c])
                    self.points.remove(collinear_higher[c])

                collinear_crossroad = Point(s, town_a.y, Point.TYPE_CROSSROAD)
                crossroads.append(collinear_crossroad)
                if not (len(collinear_lower) == 0):
                    edges.append((collinear_lower[len(collinear_lower) - 1], collinear_crossroad))
                    skipped_towns.append(collinear_lower[len(collinear_lower) - 1])
                    self.points.remove(collinear_lower[len(collinear_lower) - 1])
                if not (len(collinear_higher) == 0):
                    edges.append((collinear_higher[0], collinear_crossroad))
                    skipped_towns.append(collinear_higher[0])
                    self.points.remove(collinear_higher[0])

            for city in self.points:
                if not (is_between(town_a, city, town_b)):
                    new_crossroad = Point(city.x, town_a.y, Point.TYPE_CROSSROAD)
                    crossroads.append(new_crossroad)
                    edges.append((city, new_crossroad))

            self.points += skipped_towns

        towns_beetween_a_and_b = []
        for pnt in self.points:
            if not(pnt == town_a) and not(pnt == town_b):
                if is_between(town_a, pnt, town_b):
                    towns_beetween_a_and_b.append(pnt)
        towns_beetween_a_and_b.sort(key=lambda point: point.x)

        if not(len(towns_beetween_a_and_b) == 0):
            edges.append((town_a, towns_beetween_a_and_b[0]))
            for i in range(1, len(towns_beetween_a_and_b)):
                edges.append((towns_beetween_a_and_b[i-1], towns_beetween_a_and_b[i]))
            edges.append((towns_beetween_a_and_b[len(towns_beetween_a_and_b)-1], town_b))
        else:
            edges.append((town_a, town_b))

        self.points += crossroads
        self.state = State(edges)

        for e1, e2 in edges:
            print(e1, e2)
        for c in self.points:
            print(c)

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
