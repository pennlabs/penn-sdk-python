import datetime

from nose.tools import ok_
from penn import StudySpaces


class TestStudySpaces():

    def setUp(self):
        self.studyspaces = StudySpaces()

    def test_buildings(self):
        buildings = self.studyspaces.get_buildings()
        ok_(len(buildings) > 0)
        for building in buildings:
            ok_(building["lid"] > 0)
            ok_(building["name"])
            ok_(building["service"])

    def test_room_name_mapping(self):
        mapping = self.studyspaces.get_room_id_name_mapping(2683)
        ok_(len(mapping) > 0)

    def test_rooms(self):
        """ Make sure that at least 3 buildings have at least one room. """

        now = datetime.datetime.now()
        buildings = self.studyspaces.get_buildings()
        for building in buildings[:3]:
            rooms = self.studyspaces.get_rooms(building["id"], now, now + datetime.timedelta(days=3))
            ok_(len(rooms) > 0, "The building {} does not have any rooms!".format(building))
            for room in rooms:
                ok_(room["room_id"] > 0)
                ok_(len(room["times"]) > 0)

    def test_booking(self):
        """ Test the checks before booking the room, but don't actually book a room. """

        buildings = self.studyspaces.get_buildings()
        # get the first building
        building_id = buildings[0]["id"]

        now = datetime.datetime.now()
        rooms = self.studyspaces.get_rooms(building_id, now, now + datetime.timedelta(days=1))

        if not rooms:
            return

        # get the first room
        room_id = rooms[0]["room_id"]
        room_time = rooms[0]["times"][0]

        result = self.studyspaces.book_room(
            building_id,
            room_id,
            datetime.datetime.strptime(room_time["start"][:-6], "%Y-%m-%dT%H:%M:%S"),
            datetime.datetime.strptime(room_time["end"][:-6], "%Y-%m-%dT%H:%M:%S"),
            "John",
            "Doe",
            "test@example.com",
            "Test Meeting",
            "000-000-0000",
            "2-3",
            fake=True
        )
        ok_(result)
