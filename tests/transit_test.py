import unittest
from penn import transit
import datetime
# Abuse of globals
username = None
password = None

class TestRegistrar(unittest.TestCase):

    def setUp(self):
        self.transit = transit.Transit(username, password)

    def test_lastname_search(self):
        now = datetime.datetime(2014, 9, 16, 22, 24, 52, 91243)
        yesterday = datetime.datetime(2014, 9, 15, 22, 24, 52, 91243)
        print self.transit.stoptimes(yesterday, now)



if __name__ == '__main__':
    from credentials import TRA_USERNAME, TRA_PASSWORD
    username = TRA_USERNAME
    password = TRA_PASSWORD

    if username is None or password is None:
        print "You must provide a valid API username and password to run these tests"
    else:
        unittest.main()
