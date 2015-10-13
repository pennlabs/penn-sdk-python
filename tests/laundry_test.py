import unittest
from penn import Laundry


class TestLaundry(unittest.TestCase):

    def setUp(self):
        self.laundry = Laundry()

    def test_all(self):
        data = self.laundry.all_status()
        self.assertEquals('Class of 1925 House', data[0]['name'])
        self.assertEquals(55, len(data))

    def test_single_hall(self):
        for i in range(5):
            data = self.laundry.hall_status(i)
            self.assertEquals(data['machines'][0]['number'], '1')
