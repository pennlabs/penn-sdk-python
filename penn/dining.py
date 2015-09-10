"""A module for consuming the Penn Dining API"""
from os import path
from base import WrapperBase


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/dining/"
ENDPOINTS = {
    'MENUS': BASE_URL + 'menus',
    'VENUES': BASE_URL + 'venues',
}

# Normalization for dining menu data
def normalize_weekly(data):
    if not "tblMenu" in data["result_data"]["Document"]:
        data["result_data"]["Document"]["tblMenu"] = []
    if isinstance(data["result_data"]["Document"]["tblMenu"], dict):
        data["result_data"]["Document"]["tblMenu"] = [data["result_data"]["Document"]["tblMenu"]]
    for day in data["result_data"]["Document"]["tblMenu"]:
        if isinstance(day["tblDayPart"], dict):
            day["tblDayPart"] = [day["tblDayPart"]]
        for meal in day["tblDayPart"]:
            if isinstance(meal["tblStation"], dict):
                meal["tblStation"] = [meal["tblStation"]]
            for station in meal["tblStation"]:
                if isinstance(station["tblItem"], dict):
                    station["tblItem"] = [station["tblItem"]]
    return data




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
