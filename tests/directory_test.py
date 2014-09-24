import unittest
from penn import directory

# Abuse of globals
username = None
password = None

class TestRegistrar(unittest.TestCase):

    def setUp(self):
        self.dir = directory.Directory(username, password)

    def test_lastname_search(self):
        person = self.dir.search({'last_name':'Wissmann'})['result_data']
        self.assertEquals(len(person), 1)
        self.assertEquals(person[0]['detail_name'], "ALEXANDER R WISSMANN")



if __name__ == '__main__':
    from credentials import DIR_USERNAME, DIR_PASSWORD
    username = DIR_USERNAME
    password = DIR_PASSWORD

    if username is None or password is None:
        print "You must provide a valid API username and password to run these tests"
    else:
        unittest.main()
