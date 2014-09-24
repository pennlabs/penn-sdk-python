"""A module for consuming the Penn Registrar API"""
from os import path
import requests


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/transit/"
ENDPOINTS = {
    'APC': BASE_URL + 'apc',
    'MDT': BASE_URL + 'mdt',
    'TRANSAPC': BASE_URL + 'transapc',
    'STOPINVENTORY': BASE_URL + 'stopinventory',
    'STOPTIMES': BASE_URL + 'stoptimes'
}

class Transit(object):
    """The client for the Registrar. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn.directory import Directory
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
        """Make a signed request to the API, raise any API errors, and returning a tuple
        of (data, metadata)"""
        print params
        response = requests.get(url, params=params, headers=self.headers).json()

        if response['service_meta']['error_text']:
            raise ValueError(response['service_meta']['error_text'])

        return response


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
