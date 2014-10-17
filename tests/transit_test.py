import unittest
from penn import transit
import datetime
# Abuse of globals
username = None
password = None

class TestRegistrar(unittest.TestCase):

    def setUp(self):
        self.transit = transit.Transit(username, password)

    def test_apc(self):
        now = datetime.datetime(2014, 9, 16, 22, 24, 52, 91243)
        yesterday = datetime.datetime(2014, 9, 15, 22, 24, 52, 91243)
        data = self.transit.apc(yesterday, now)
        self.assertEquals(data['result_data'][0]['Bus'], 'T17')

    def test_mdt(self):
        now = datetime.datetime(2014, 9, 16, 22, 24, 52, 91243)
        yesterday = datetime.datetime(2014, 9, 15, 22, 24, 52, 91243)
        data = self.transit.mdt(yesterday, now)
        #  TODO: Figure this out
        self.assertEquals(len(data['result_data']), 0)

    def test_transapc(self):
        now = datetime.datetime(2014, 9, 16, 22, 24, 52, 91243)
        yesterday = datetime.datetime(2014, 9, 15, 22, 24, 52, 91243)
        data = self.transit.transapc(yesterday, now)
        self.assertEquals(data['result_data'][0]['PassengerBoardings'], 1)
        self.assertEquals(data['result_data'][0]['VehicleId'], 168)

    def test_stoptimes(self):
        now = datetime.datetime(2014, 9, 16, 22, 24, 52, 91243)
        yesterday = datetime.datetime(2014, 9, 15, 22, 24, 52, 91243)
        data = self.transit.stoptimes(yesterday, now)
        self.assertEquals(data['result_data'][0]['Dep'], '9/15/2014 10:25:54 PM')

    def test_stopinventory(self):
        now = datetime.datetime(2014, 9, 16, 22, 24, 52, 91243)
        yesterday = datetime.datetime(2014, 9, 15, 22, 24, 52, 91243)
        data = self.transit.stopinventory(yesterday, now)
        self.assertEquals(data['result_data'][0]['BusStopId'], 29184)
        self.assertEquals(data['result_data'][0]['BusStopName'], 'Pottruck Center, 3701 Walnut St')




if __name__ == '__main__':
    from credentials import TRA_USERNAME, TRA_PASSWORD
    username = TRA_USERNAME
    password = TRA_PASSWORD

    if username is None or password is None:
        print "You must provide a valid API username and password to run these tests"
    else:
        unittest.main()
