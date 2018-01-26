import datetime
import pytz

from nose.tools import ok_
from penn import StudySpaces


class TestStudySpaces():

    def setUp(self):
        self.studyspaces = StudySpaces()

    def test_buildings(self):
        buildings = self.studyspaces.get_buildings()
        ok_(len(buildings) > 0)

    def test_room_name_mapping(self):
        mapping = self.studyspaces.get_room_id_name_mapping(2683)
        ok_(len(mapping) > 0)

    def test_rooms(self):
        now = pytz.timezone("US/Eastern").localize(datetime.datetime.now())
        rooms = self.studyspaces.get_rooms(2683, now, now + datetime.timedelta(days=3))
        ok_(len(rooms) > 0)
