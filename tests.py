import unittest
import math

from algorithm import Algorithm, Point, State


class AlgorithmTest(unittest.TestCase):
    def test_fitness_function(self):
        alg = Algorithm([(0, 0), (0, 2), (0, 3), (1, 1)])

        alg.points = [Point(0, 0, Point.TYPE_TOWN), Point(0, 1, Point.TYPE_TOWN), Point(0, 2, Point.TYPE_TOWN),
                      Point(0, 3, Point.TYPE_TOWN), Point(1, 3, Point.TYPE_TOWN)]

        state = State([
            (alg.points[0], alg.points[1]),
            (alg.points[1], alg.points[2]),
            (alg.points[2], alg.points[3]),
            (alg.points[0], alg.points[4]),
            (alg.points[4], alg.points[3]),
        ])

        fitness = alg.fitness_function(state)
        self.assertAlmostEqual(fitness, 1 + 1 + 1 + 1 + math.sqrt(1 + 3 ** 2) +
                               1 + 2 + 3 + math.sqrt(10) + 1 + 2 + 3 + 1 + 2 + 1,
                               places=2)


if __name__ == 'main':
    unittest.main()

