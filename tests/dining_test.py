import unittest
from penn import dining
import json


class TestDining(unittest.TestCase):

    def setUp(self):
        from .credentials import DIN_USERNAME, DIN_PASSWORD
        username = DIN_USERNAME
        password = DIN_PASSWORD
        self.assertFalse(username is None or password is None)
        self.din = dining.Dining(username, password)

#     def test_dining(self):
#         venues = self.din.venues()['result_data']['document']['venue']
#         venues = venues[0]
#         self.assertTrue(len(venues) > 0)
#         id = str(venues["id"])
#         data = self.din.menu_daily(id)
#         dayPart = data["result_data"]["Document"]["tblMenu"]["tblDayPart"]
#         if len(dayPart) > 0:
#             self.assertTrue(len(dayPart[0]) >= 2)

#     def test_dining_normalization(self):
#         data = self.din.menu_daily("593")
#         self.assertTrue(isinstance(
#             data["result_data"]["Document"]["tblMenu"]["tblDayPart"], list))

#     def test_dining_venue_normalization(self):
#         data = self.din.venues()
#         self.assertTrue(isinstance(
#             data["result_data"]["document"]["venue"][2]["dateHours"], list))

#     def test_weekly_normalization_unit(self):
#         json_data = open("tests/menu_data.json").read()
#         data = json.loads(json_data)

#         self.assertTrue(isinstance(
#             data["result_data"]["Document"]["tblMenu"][0]["tblDayPart"]["tblStation"][6]["tblItem"], dict))

#         self.assertTrue(isinstance(
#             data["result_data"]["Document"]["tblMenu"][5]["tblDayPart"][2]["tblStation"], dict))

#         new_data = dining.normalize_weekly(data)

#         self.assertTrue(isinstance(
#             new_data["result_data"]["Document"]["tblMenu"][0]["tblDayPart"][0]["tblStation"][6]["tblItem"], list))

#         self.assertTrue(isinstance(
#             new_data["result_data"]["Document"]["tblMenu"][5]["tblDayPart"][2]["tblStation"], list))

#         self.assertTrue(isinstance(
#             new_data["result_data"]["Document"]["tblMenu"][0]["tblDayPart"], list))


class TestDiningV2(unittest.TestCase):

    def setUp(self):
        from .credentials import DIN_USERNAME, DIN_PASSWORD
        username = DIN_USERNAME
        password = DIN_PASSWORD
        self.assertFalse(username is None or password is None)
        self.din = dining.DiningV2(username, password)

#     def test_dining(self):
#         venues = self.din.venues()['result_data']['document']['venue']
#         venues = venues[0]
#         self.assertTrue(len(venues) > 0)

#     def test_hours(self):
#         commons = self.din.hours("593")['result_data']['cafes']['593']
#         self.assertEquals("1920 Commons", commons['name'])
#         self.assertTrue(len(commons['days']) > 2)

#     def test_menu(self):
#         commons = self.din.menu("593", "2016-02-07")['result_data']['days'][0]
#         self.assertEquals(commons['date'], "2016-02-07")

#     def test_item(self):
#         tomato_sauce = self.din.item("3899220")['result_data']['items']['3899220']
#         self.assertEquals(tomato_sauce['label'], "tomato tzatziki sauce and pita")
