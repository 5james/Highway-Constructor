import unittest
import math

from algorithm import Algorithm, State, Point


class AlgorithmTest(unittest.TestCase):
    pass
    # def test_fitness_function(self):
        # alg = Algorithm([(0, 1), (6, 1), (3, 0), (3, 2)])

        # fitness = alg.fitness_function(alg.state)
        # self.assertAlmostEqual(fitness, (6 + 1 + 1) + (6 + 4 + 4 + 2 + 4 + 4), places=2)


class StateTest(unittest.TestCase):
    def test_sanitize_edges(self):
        points = [Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 0), Point(3, 0)]
        edges = [(points[0], points[1]), (points[2], points[1]), (points[3], points[1]),
                 (points[4], points[1]), (points[2], points[3])]
        state = State(edges)

        self.assertCountEqual(state.points, points)

        new_edges = state._sanitize_edges([(points[0], points[4])])
        self.assertCountEqual(
            new_edges,
            [(points[0], points[2]), (points[3], points[4])]
        )

        points = [Point(0, 0), Point(1, 0), Point(0, 1), Point(2, 0)]
        edges = [(points[0], points[1]), (points[0], points[2]), (points[2], points[3])]

        state = State(edges)

        self.assertCountEqual(state.points, points)

        new_edges = state._sanitize_edges([(points[0], points[3])])

        self.assertCountEqual(
            new_edges,
            [(points[1], points[3])]
        )

    def test_add_crossroads(self):
        points = [Point(0, 1), Point(1, 2), Point(2, 1), Point(1, 0)]

        current_edges = [(points[0], points[1]), (points[2], points[1]), (points[3], points[1])]
        new_edges = [(points[0], points[2])]

        new_edges = State._add_crossroads(new_edges, current_edges)

        self.assertEqual(len(new_edges), 6)
        self.assertEqual(len([edge for edge in new_edges
                              if edge[0].type == Point.TYPE_CROSSROAD or edge[1].type == Point.TYPE_CROSSROAD]),
                         4)

    def test_get_neighbours(self):
        points = [Point(0, 0), Point(0, 1), Point(1, 0)]
        edges = [(points[0], points[1]), (points[0], points[2])]

        state = State(edges)

        neighbours = state.get_neighbours()

        # for neighbour in neighbours:
        #     print('neighbour')
        #     for edge in neighbour.edges:
        #         print(str(edge[0]) + ' ' + str(edge[1]))

        self.assertEqual(len(neighbours), 1)
        self.assertCountEqual(neighbours[0].edges, [(points[0], points[1]), (points[0], points[2]),
                                                    (points[1], points[2])])

        edges = [(points[0], points[1]), (points[0], points[2]), (points[1], points[2])]

        state = State(edges)

        neighbours = state.get_neighbours()

        self.assertEqual(len(neighbours), 3)
        for neighbour in neighbours:
            self.assertEqual(len(neighbour.edges), 2)

if __name__ == 'main':
    unittest.main()
