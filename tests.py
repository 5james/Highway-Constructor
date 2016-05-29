import unittest
import math

from algorithm import Algorithm, Point, State


class AlgorithmTest(unittest.TestCase):
    def test_fitness_function(self):
        alg = Algorithm([(0, 0), (0, 2), (0, 3), (1, 1)])

        fitness = alg.fitness_function(alg.state)
        self.assertAlmostEqual(fitness, 1 + 1 + 1 + 1 + math.sqrt(1 + 3 ** 2) +
                               1 + 2 + 3 + math.sqrt(10) + 1 + 2 + 3 + 1 + 2 + 1,
                               places=2)


if __name__ == 'main':
    unittest.main()

