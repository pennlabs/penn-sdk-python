"""A module for consuming the Penn Registrar API"""
from os import path
import requests
from base import WrapperBase


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/dining/"
ENDPOINTS = {
    'MENUS': BASE_URL + 'menus',
    'VENUES': BASE_URL + 'venues',
}

class Dining(WrapperBase):
    """The client for the Registrar. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn.dining import Dining
      >>> din = Dining('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """
    def venues(self):
        """Get a list of all venue objects.

          >>> venues = din.venues()
        """

        response = self._request(ENDPOINTS['VENUES'])
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
        return response

    def menu_weekly(self, building_id):
        """Get an array of menu objects corresponding to the weekly menu for the
        venue with building_id.

        :param building_id:
            A string representing the id of a building, e.g. "abc".

        >>> commons_week = din.menu_weekly("593")
        """
        response = self._request(path.join(ENDPOINTS['MENUS'], 'weekly', str(building_id)))
        return response

