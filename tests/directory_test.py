import unittest
from penn import directory


class TestDirectory(unittest.TestCase):

    def setUp(self):
        from credentials import DIR_USERNAME, DIR_PASSWORD
        username = DIR_USERNAME
        password = DIR_PASSWORD
        self.assertFalse(username is None or password is None)
        self.dir = directory.Directory(username, password)

    def test_lastname_search(self):
        person = self.dir.detail_search({'last_name':'Wissmann'})['result_data']
        self.assertEquals(len(person), 1)
        self.assertEquals(person[0]['result_data'][0]['detail_name'], "ALEXANDER R WISSMANN")

    def test_faculty_name_not_standardized(self):
        fac = self.dir.search({'first_name': 'kostas'})
        self.assertEquals(fac['result_data'][0]['list_name'], "DANIILIDIS, KONSTANTINOS ")

    def test_faculty_name_standardized(self):
        fac = self.dir.search({'first_name': 'kostas'}, standardize=True)
        self.assertEquals(fac['result_data'][0]['list_name'], "Konstantinos Daniilidis")

    def test_email_not_standardized(self):
        email = self.dir.search({'first_name': 'amy', 'last_name': 'gallagher'})
        self.assertEqual(email['result_data'][0]['list_email'], 'Amy.Gallagher@uphs.upenn.edu')

    def test_email_standardized(self):
        email = self.dir.search({'first_name': 'amy', 'last_name': 'gallagher'}, standardize=True)
        self.assertEqual(email['result_data'][0]['list_email'], 'amy.gallagher@uphs.upenn.edu')

    def test_afl_not_standardized(self):
        afl = self.dir.search({'first_name': 'kostas'})
        self.assertEqual(afl['result_data'][0]['list_affiliation'], 'Faculty - ASSOC PROFESSOR')

    def test_afl_standardized(self):
        afl = self.dir.search({'first_name': 'kostas'}, standardize=True)
        self.assertEqual(afl['result_data'][0]['list_affiliation'], 'ASSOC PROFESSOR')
