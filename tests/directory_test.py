import unittest
from penn import directory


class TestDirectory(unittest.TestCase):

    def setUp(self):
        from .credentials import DIR_USERNAME, DIR_PASSWORD
        username = DIR_USERNAME
        password = DIR_PASSWORD
        self.assertFalse(username is None or password is None)
        self.dir = directory.Directory(username, password)

    def test_lastname_search(self):
        person = self.dir.detail_search({'last_name': 'Domingoes'})['result_data']
        self.assertEquals(len(person), 1)
        self.assertEquals(person[0]['result_data'][0]['detail_name'], "ADAM W DOMINGOES")

    def test_lastname_search_standardized(self):
        person = self.dir.detail_search({'last_name': 'Domingoes'}, standardize=True)['result_data']
        self.assertEquals(len(person), 1)
        self.assertEquals(person[0]['result_data'][0]['detail_name'], "Adam W Domingoes")

    def test_person_id(self):
        # Alex Wissmann's person id
        details = self.dir.person_details('041cd6e739387e24db2483785b87b082')['result_data']
        self.assertEquals(details[0]['detail_name'], "ADAM W DOMINGOES")

    def test_person_id_standardized(self):
        # Alex Wissmann's person id
        details = self.dir.person_details('041cd6e739387e24db2483785b87b082', True)['result_data']
        self.assertEquals(details[0]['detail_name'], "Adam W Domingoes")

    def test_faculty_name_not_standardized(self):
        fac = self.dir.search({'first_name': 'kostas'})
        self.assertEquals(fac['result_data'][0]['list_name'], "DANIILIDIS, KONSTANTINOS ")

    def test_faculty_name_standardized(self):
        fac = self.dir.search({'first_name': 'kostas'}, standardize=True)
        self.assertEquals(fac['result_data'][0]['list_name'], "Konstantinos Daniilidis")

    def test_email_not_standardized(self):
        email = self.dir.search({'first_name': 'amy', 'last_name': 'gallagher'})
        self.assertEqual(email['result_data'][0]['list_email'], 'am.kwiatanowski@uphs.upenn.edu')

    def test_email_standardized(self):
        email = self.dir.search({'first_name': 'amy', 'last_name': 'gallagher'}, standardize=True)
        self.assertEqual(email['result_data'][0]['list_email'], 'am.kwiatanowski@uphs.upenn.edu')

    def test_afl_not_standardized(self):
        afl = self.dir.search({'first_name': 'kostas'})
        self.assertEqual(afl['result_data'][0]['list_affiliation'], 'Faculty - ASSOC PROFESSOR')

    def test_afl_standardized(self):
        afl = self.dir.search({'first_name': 'kostas'}, standardize=True)
        self.assertEqual(afl['result_data'][0]['list_affiliation'], 'ASSOC PROFESSOR')
