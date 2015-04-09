import unittest
from penn import Laundry


class TestLaundry(unittest.TestCase):

    def setUp(self):
        self.laundry = Laundry()

    def test_all(self):
        data = self.laundry.all_status()
        self.assertEquals('DuBois House', data[0]['name'])
        self.assertEquals(54, len(data))


    def test_map(self):
        for i in xrange(5):
            data = self.laundry.hall_status(i)
            self.assertEquals(data['machines'][0]['number'], '1')

