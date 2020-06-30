import unittest

from penn.fitness import Fitness


class TestFitness(unittest.TestCase):

    def setUp(self):
        from .credentials import FITNESS_TOKEN

        self.fitness = Fitness(FITNESS_TOKEN)

    def test_usage(self):
        usage = self.fitness.get_usage()
        self.assertTrue(len(usage) > 0)
        for item in usage:
            self.assertTrue("name" in item)
            self.assertTrue("open" in item)
            self.assertTrue("updated" in item)
            self.assertTrue("percent" in item)

    # def test_schedule(self):
    #     schedule = self.fitness.get_schedule()
    #     self.assertTrue(len(schedule) > 0)
