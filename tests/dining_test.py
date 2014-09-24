import unittest
import json
from penn import dining

# Abuse of globals
username = None
password = None

class TestRegistrar(unittest.TestCase):

    def setUp(self):
        self.din = dining.Dining(username, password)

    def test_dining(self):
        venues = self.din.venues()['result_data']['document']['venue']
        venues = venues[0]
        self.assertTrue(len(venues) > 0)
        id = str(venues["id"])
        data = self.din.menu_weekly(id)
        self.assertEquals(len(data["result_data"]["Document"]["tblMenu"]), 7)




if __name__ == '__main__':
    from credentials import DIN_USERNAME, DIN_PASSWORD
    username = DIN_USERNAME
    password = DIN_PASSWORD

    if username is None or password is None:
        print "You must provide a valid API username and password to run these tests"
    else:
        unittest.main()
