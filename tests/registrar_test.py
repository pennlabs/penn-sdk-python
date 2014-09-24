import unittest
from penn import registrar

# Abuse of globals
username = None
password = None

class TestRegistrar(unittest.TestCase):

    def setUp(self):
        self.reg = registrar.Registrar(username, password)

    def test_section(self):
        acct101001 = self.reg.section('acct', '101', '001')
        self.assertEqual(acct101001['section_id'], 'ACCT101001')

    def test_department(self):
        cis = self.reg.department('cis')
        next(cis) # Should be an iterator
        self.assertTrue(len(list(cis)) > 20) # Should have multiple pages of items

    def test_course(self):
        cis120 = self.reg.course('cis', '120')
        self.assertEqual(cis120['course_id'], 'CIS 120')

    def test_search(self):
        cis_search = self.reg.search({'course_id': 'cis'})
        cis_dept = self.reg.department('cis')
        self.assertTrue(len(list(cis_search)) >= len(list(cis_dept)) > 20)
        # There will always be a Kors class at Penn
        sub_search = self.reg.search({'course_id': 'hist', 'instructor': 'Kors'})
        self.assertTrue(len(list(sub_search)))

    def test_search_params(self):
        params = self.reg.search_params()
        self.assertTrue('activity_map' in params)


if __name__ == '__main__':
    from credentials import REG_USERNAME, REG_PASSWORD
    username = REG_USERNAME
    password = REG_PASSWORD

    if username is None or password is None:
        print "You must provide a valid API username and password to run these tests"
    else:
        unittest.main()
