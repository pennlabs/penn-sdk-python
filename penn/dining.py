"""A module for consuming the Penn Dining API"""
from os import path
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


# Normalization for dining menu data
def normalize_weekly(data):
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
        response = self._request(ENDPOINTS['VENUES'])
        # Normalize `dateHours` to array
        for venue in response["result_data"]["document"]["venue"]:
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
        response = self._request(
            path.join(ENDPOINTS['MENUS'], 'daily', str(building_id))
        )
        # Normalize `tblDayPart` and `tblItem` to array
        meals = response["result_data"]["Document"]["tblMenu"]["tblDayPart"]
        if isinstance(meals, dict):
            response["result_data"]["Document"]["tblMenu"]["tblDayPart"] = [meals]
        for meal in response["result_data"]["Document"]["tblMenu"]["tblDayPart"]:
            if isinstance(meal["tblStation"], dict):
                meal["tblStation"] = [meal["tblStation"]]
            for station in meal["tblStation"]:
                if isinstance(station["tblItem"], dict):
                    station["tblItem"] = [station["tblItem"]]
        return response

    def menu_weekly(self, building_id):
        """Get an array of menu objects corresponding to the weekly menu for the
        venue with building_id.

        :param building_id:
            A string representing the id of a building, e.g. "abc".

        >>> commons_week = din.menu_weekly("593")
        """
        response = self._request(path.join(ENDPOINTS['MENUS'], 'weekly', str(building_id)))
        return normalize_weekly(response)
