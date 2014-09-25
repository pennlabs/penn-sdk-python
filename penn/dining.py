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
    def __init__(self, bearer, token):
        self.bearer = bearer
        self.token = token

    @property
    def headers(self):
        """The HTTP headers needed for signed requests"""
        return {
            "Authorization-Bearer": self.bearer,
            "Authorization-Token": self.token,
        }

    def _request(self, url, params=None):
        """Make a signed request to the API, raise any API errors, and returning
        a tuple of (data, metadata)"""
        response = requests.get(url, params=params, headers=self.headers).json()

        if response['service_meta']['error_text']:
            raise ValueError(response['service_meta']['error_text'])

        return response

    def venues(self):
        """Get a list of all venue objects.

          >>> venues = din.venues()
        """

        response = self._request(ENDPOINTS['VENUES'])
        return response

    def menu_daily(self, building_id):
        """Get a menu object corresponding to the daily menu for the
        venue with building_id.

        :param building_id: The id of the building. Should be a string.


        >>> commons_today = din.menu_daily("593")
        """
        response = self._request(
            path.join(ENDPOINTS['MENUS'], 'daily', str(building_id))
        )
        return response

    def menu_weekly(self, building_id):
        """Get an array of menu objects corresponding to the weekly menu for the
        venue with building_id.

        :param building_id: The id of the building. Should be a string.

        >>> commons_week = din.menu_weekly("593")
        """
        response = self._request(path.join(ENDPOINTS['MENUS'], 'weekly', str(building_id)))
        return response

