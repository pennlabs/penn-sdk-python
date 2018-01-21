from nose.tools import ok_
from penn import StudySpaces
import datetime


class TestStudySpaces():

    def setUp(self):
        self.studyspaces = StudySpaces()

    def test_buildings(self):
        buildings = self.studyspaces.get_buildings()
        ok_(len(buildings) > 0)

    def test_rooms(self):
        now = datetime.datetime.now()
        rooms = self.studyspaces.get_rooms(2683, now, now + datetime.timedelta(days=3))
        ok_(len(rooms) > 0)
