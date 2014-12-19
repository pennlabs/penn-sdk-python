import unittest
from penn import dining


class TestDining(unittest.TestCase):

    def setUp(self):
        from credentials import DIN_USERNAME, DIN_PASSWORD
        username = DIN_USERNAME
        password = DIN_PASSWORD
        self.assertFalse(username is None or password is None)
        self.din = dining.Dining(username, password)

    def test_dining(self):
        venues = self.din.venues()['result_data']['document']['venue']
        venues = venues[0]
        self.assertTrue(len(venues) > 0)
        id = str(venues["id"])
        data = self.din.menu_weekly(id)
        self.assertTrue(len(data["result_data"]["Document"]["tblMenu"]) > 4)
