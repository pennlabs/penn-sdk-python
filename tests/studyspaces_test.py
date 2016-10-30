from nose.tools import ok_
from penn import StudySpaces


class TestStudySpaces():

    def setUp(self):
        self.studyspaces = StudySpaces()

    def test_json(self):
        json_id = self.studyspaces.get_id_json()
        ok_(len(json_id) > 0)
        for i in json_id:
            ok_(i['id'] > 0)
            ok_(i['name'] != '')
            ok_(i['url'] != '')

    def test_extraction(self):
        dict_id = self.studyspaces.get_id_dict()
        ok_(len(dict_id) > 0)
        for i in dict_id:
            s = self.studyspaces.extract_times(1799, "2016-11-11",
                                                     "Van Pelt-Dietrich Library Center Group Study Rooms")
            ok_("building" in s)
            ok_("start_time" in s)
            ok_("end_time" in s)
            ok_("date" in s)
            ok_("roomname" in s)
