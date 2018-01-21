"""A module for consuming the Penn Dining API"""
import datetime
from .base import WrapperBase


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/dining/"
V2_BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/dining/v2/?service="

ENDPOINTS = {
    'MENUS': BASE_URL + 'menus',
    'VENUES': BASE_URL + 'venues',
}

V2_ENDPOINTS = {
    'VENUES': V2_BASE_URL + 'venues',
    'HOURS': V2_BASE_URL + 'cafes&cafe=',
    'MENUS': V2_BASE_URL + 'menus&cafe=',
    'ITEMS': V2_BASE_URL + 'items&item='
}

VENUE_NAMES = {
    '593': '1920 Commons',
    '636': 'Hill House',
    '637': 'Kings Court English House',
    '638': 'Kosher Dining at Falk'
}


def normalize_weekly(data):
    """Normalization for dining menu data"""
    if "tblMenu" not in data["result_data"]["Document"]:
        data["result_data"]["Document"]["tblMenu"] = []
    if isinstance(data["result_data"]["Document"]["tblMenu"], dict):
        data["result_data"]["Document"]["tblMenu"] = [data["result_data"]["Document"]["tblMenu"]]
    for day in data["result_data"]["Document"]["tblMenu"]:
        if "tblDayPart" not in day:
            continue
        if isinstance(day["tblDayPart"], dict):
            day["tblDayPart"] = [day["tblDayPart"]]
        for meal in day["tblDayPart"]:
            if isinstance(meal["tblStation"], dict):
                meal["tblStation"] = [meal["tblStation"]]
            for station in meal["tblStation"]:
                if isinstance(station["tblItem"], dict):
                    station["tblItem"] = [station["tblItem"]]
    return data


def get_meals(v2_response, building_id):
    """Extract meals into old format from a DiningV2 JSON response"""
    result_data = v2_response["result_data"]
    meals = []
    day_parts = result_data["days"][0]["cafes"][building_id]["dayparts"][0]
    for meal in day_parts:
        stations = []
        for station in meal["stations"]:
            items = []
            for item_id in station["items"]:
                item = result_data["items"][item_id]
                new_item = {}
                new_item["txtTitle"] = item["label"]
                new_item["txtPrice"] = ""
                new_item["txtNutritionInfo"] = ""
                new_item["txtDescription"] = item["description"]
                new_item["tblSide"] = ""
                new_item["tblFarmToFork"] = ""
                attrs = [{"description": item["cor_icon"][attr]} for attr in item["cor_icon"]]
                if len(attrs) == 1:
                    new_item["tblAttributes"] = {"txtAttribute": attrs[0]}
                elif len(attrs) > 1:
                    new_item["tblAttributes"] = {"txtAttribute": attrs}
                else:
                    new_item["tblAttributes"] = ""
                if isinstance(item["options"], list):
                    item["options"] = {}
                if "values" in item["options"]:
                    for side in item["options"]["values"]:
                        new_item["tblSide"] = {"txtSideName": side["label"]}
                items.append(new_item)
            stations.append({"tblItem": items, "txtStationDescription": station["label"]})
        meals.append({"tblStation": stations, "txtDayPartDescription": meal["label"]})
    return meals


class DiningV2(WrapperBase):
    """The client for the Registrar. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn import DiningV2
      >>> din = DiningV2('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """
    def venues(self):
        """Get a list of all venue objects.

          >>> venues = din.venues()
        """
        response = self._request(V2_ENDPOINTS['VENUES'])
        return response

    def hours(self, venue_id):
        """Get the list of hours for the venue corresponding to
        venue_id.

        :param venue_id:
          A string representing the id of a venue, e.g. "abc".


        >>> commons_hours = din.hours("593")
        """
        response = self._request(V2_ENDPOINTS['HOURS'] + venue_id)
        return response

    def menu(self, venue_id, date):
        """Get the menu for the venue corresponding to venue_id,
        on date.

        :param venue_id:
          A string representing the id of a venue, e.g. "abc".
        :param date:
          A string representing the date of a venue's menu, e.g. "2015-09-20".


        >>> commons_menu = din.menu("593", "2015-09-20")
        """
        query = "&date=" + date
        response = self._request(V2_ENDPOINTS['MENUS'] + venue_id + query)
        return response

    def item(self, item_id):
        """Get a description of the food item corresponding to item_id.

        :param item_id:
          A string representing the id of an item, e.g. "3899220".


        >>> tomato_sauce = din.item("3899220")
        """
        response = self._request(V2_ENDPOINTS['ITEMS'] + item_id)
        return response


class Dining(WrapperBase):
    """The client for the Registrar. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn import Dining
      >>> din = Dining('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """
    def venues(self):
        """Get a list of all venue objects.

          >>> venues = din.venues()
        """
        response = self._request(V2_ENDPOINTS['VENUES'])
        # Normalize `dateHours` to array
        for venue in response["result_data"]["document"]["venue"]:
            if venue.get("id") in VENUE_NAMES:
                venue["name"] = VENUE_NAMES[venue.get("id")]
            if isinstance(venue.get("dateHours"), dict):
                venue["dateHours"] = [venue["dateHours"]]
            if "dateHours" in venue:
                for dh in venue["dateHours"]:
                    if isinstance(dh.get("meal"), dict):
                        dh["meal"] = [dh["meal"]]
        return response

    def menu_daily(self, building_id):
        """Get a menu object corresponding to the daily menu for the
        venue with building_id.

        :param building_id:
          A string representing the id of a building, e.g. "abc".


        >>> commons_today = din.menu_daily("593")
        """
        today = str(datetime.date.today())
        v2_response = DiningV2(self.bearer, self.token).menu(building_id, today)
        response = {'result_data': {'Document': {}}}
        response["result_data"]["Document"]["menudate"] = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%-m/%d/%Y')
        if building_id in VENUE_NAMES:
            response["result_data"]["Document"]["location"] = VENUE_NAMES[building_id]
        else:
            response["result_data"]["Document"]["location"] = v2_response["result_data"]["days"][0]["cafes"][building_id]["name"]
        response["result_data"]["Document"]["tblMenu"] = {"tblDayPart": get_meals(v2_response, building_id)}
        return response

    def menu_weekly(self, building_id):
        """Get an array of menu objects corresponding to the weekly menu for the
        venue with building_id.

        :param building_id:
            A string representing the id of a building, e.g. "abc".

        >>> commons_week = din.menu_weekly("593")
        """
        din = DiningV2(self.bearer, self.token)
        response = {'result_data': {'Document': {}}}
        days = []
        for i in range(7):
            date = str(datetime.date.today() + datetime.timedelta(days=i))
            v2_response = din.menu(building_id, date)
            if building_id in VENUE_NAMES:
                response["result_data"]["Document"]["location"] = VENUE_NAMES[building_id]
            else:
                response["result_data"]["Document"]["location"] = v2_response["result_data"]["days"][0]["cafes"][building_id]["name"]
            formatted_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%-m/%d/%Y')
            days.append({"tblDayPart": get_meals(v2_response, building_id), "menudate": formatted_date})
        response["result_data"]["Document"]["tblMenu"] = days
        return normalize_weekly(response)
