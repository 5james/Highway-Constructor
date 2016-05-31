import unittest
import math

from algorithm import Algorithm, State, Point


class AlgorithmTest(unittest.TestCase):
    # def test_fitness_function(self):
    #     alg = Algorithm([(0, 0), (0, 2), (0, 3), (1, 1)])
    #
    #     fitness = alg.fitness_function(alg.state)
    #     self.assertAlmostEqual(fitness, 1 + 1 + 1 + 1 + math.sqrt(1 + 3 ** 2) +
    #                            1 + 2 + 3 + math.sqrt(10) + 1 + 2 + 3 + 1 + 2 + 1,
    #                            places=2)

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

if __name__ == 'main':
    unittest.main()
