"""A module for consuming the Penn Registrar API"""
from os import path
import requests
from base import WrapperBase

BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/transit/"
ENDPOINTS = {
    'APC': BASE_URL + 'apc',
    'MDT': BASE_URL + 'mdt',
    'TRANSAPC': BASE_URL + 'transapc',
    'STOPINVENTORY': BASE_URL + 'stopinventory',
    'STOPTIMES': BASE_URL + 'stoptimes'
}

class Transit(WrapperBase):
    """The client for Transit. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn.transit import Transit
      >>> trans = Transit('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """

    def formatDate(self, date):
        #print date.strftime("%d/%m/%Y")+ "%20" + date.strftime("%H24:%M:%S")
        return date.strftime("%m/%d/%Y")+ " " + date.strftime("%H:%M:%S")

    def apc(self, start_date, end_date):
        """Return a list of venue objects.


        >>> venues = din.venues()
        """
        params = {
            'start': self.formatDate(start_date),
            'end': self.formatDate(end_date)
        }
        response = self._request(ENDPOINTS['APC'], params)
        return response;

    def mdt(self, start_date, end_date):
        """Return a list of venue objects.


        >>> venues = din.venues()
        """
        params = {
            'start': self.formatDate(start_date),
            'end': self.formatDate(end_date)
        }
        response = self._request(ENDPOINTS['MDT'], params)
        return response;

    def transapc(self, start_date, end_date):
        """Return a list of venue objects.


        >>> venues = din.venues()
        """
        params = {
            'start': self.formatDate(start_date),
            'end': self.formatDate(end_date)
        }
        response = self._request(ENDPOINTS['TRANSAPC'], params)
        return response;

    def stopinventory(self, start_date, end_date):
        """Return a list of venue objects.


        >>> venues = din.venues()
        """
        params = {
            'start': self.formatDate(start_date),
            'end': self.formatDate(end_date)
        }
        response = self._request(ENDPOINTS['STOPINVENTORY'], params)
        return response;

    def stoptimes(self, start_date, end_date):
        """Return a list of venue objects.


        >>> venues = din.venues()
        """
        params = {
            'start': self.formatDate(start_date),
            'end': self.formatDate(end_date)
        }
        response = self._request(ENDPOINTS['STOPTIMES'], params)
        return response;
