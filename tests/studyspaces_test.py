from nose.tools import ok_
from penn import StudySpaces


class TestStudySpaces():

    def setUp(self):
        from .credentials import LIBCAL_ID, LIBCAL_SECRET
        self.studyspaces = StudySpaces(LIBCAL_ID, LIBCAL_SECRET)

    def test_buildings(self):
        buildings = self.studyspaces.get_buildings()
        ok_(len(buildings) > 0)
        for location in buildings:
            ok_("lid" in location)
            ok_("name" in location)

    def test_rooms(self):
        buildings = self.studyspaces.get_buildings()
        rooms = self.studyspaces.get_rooms(buildings[0]["lid"])
        ok_("id" in rooms)
        ok_(len(rooms["categories"]) > 0)

    def test_booking(self):
        buildings = self.studyspaces.get_buildings()
        rooms = self.studyspaces.get_rooms(buildings[0]["lid"])
        room = rooms["categories"][0]["rooms"][0]
        item = room["id"]
        result = self.studyspaces.book_room(
            item=item,
            start=room["availability"][0]["from"],
            end=room["availability"][0]["to"],
            fname="First Name",
            lname="Last Name",
            email="test@pennlabs.org",
            nickname="Test Booking",
            custom={
                "q2533": "000-000-0000",
                "q2555": "2-3"
            },
            test=True
        )
        ok_("success" in result)
