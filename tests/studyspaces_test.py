from nose.tools import ok_
from penn import StudySpaces
import datetime


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
        d = datetime.datetime.now() + datetime.timedelta(days=1)
        next_date = d.strftime("%Y-%m-%d")
        s = self.studyspaces.extract_times(1799, next_date, "Van Pelt-Dietrich Library Center Group Study Rooms")
        for i in s:
            ok_("building" in i)
            ok_("start_time" in i)
            ok_("end_time" in i)
            ok_("date" in i)
            ok_("room_name" in i)
