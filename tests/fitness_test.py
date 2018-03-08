import unittest

from penn.fitness import Fitness


class TestFitness(unittest.TestCase):

    def setUp(self):
        self.fitness = Fitness()

    def test_usage(self):
        usage = self.fitness.get_usage()
        self.assertTrue(len(usage) > 0)
        for item in usage:
            self.assertTrue("name" in item)
            self.assertTrue("open" in item)
            self.assertTrue("updated" in item)
            self.assertTrue("percent" in item)
