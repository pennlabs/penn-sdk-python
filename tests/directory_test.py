import unittest
from penn import directory

# Abuse of globals
username = None
password = None

class TestDirectory(unittest.TestCase):

    def setUp(self):
        self.assertFalse(username is None or password is None)
        self.dir = directory.Directory(username, password)

    def test_lastname_search(self):
        person = self.dir.detail_search({'last_name':'Wissmann'})['result_data']
        self.assertEquals(len(person), 1)
        self.assertEquals(person[0]['detail_name'], "ALEXANDER R WISSMANN")



if __name__ == '__main__':
    from credentials import DIR_USERNAME, DIR_PASSWORD
    username = DIR_USERNAME
    password = DIR_PASSWORD

    unittest.main()
