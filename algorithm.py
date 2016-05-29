import math
import networkx


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

    def fitness_function(self, state):
        graph = networkx.Graph()

        for edge in state.edges:
            graph.add_edge(edge[0], edge[1], {'weight': Algorithm.distance(edge[0], edge[1])})

        towns = [point for point in self.points if point.type == Point.TYPE_TOWN]

        paths_length = 0
        for i in range(0, len(towns)):
            for j in range(i + 1, len(towns)):
                paths_length += networkx.shortest_path_length(graph, source=towns[i], target=towns[j], weight='weight')

        roads_length = sum([data['weight'] for node_a, node_b, data in graph.edges(data=True)])

        return self.roads_length_factor * roads_length + self.paths_length_factor * paths_length

    @staticmethod
    def distance(point_a, point_b):
        return math.sqrt((point_b.x - point_a.x) ** 2 + (point_b.y - point_a.y) ** 2)
