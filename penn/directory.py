"""A module for consuming the Penn Registrar API"""
from os import path
import requests


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/"
ENDPOINTS = {
    'SEARCH': BASE_URL + 'directory',
    'DETAILS': BASE_URL + 'directory_person_details',
}

class Directory(object):
    """The client for the Directory. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn.directory import Directory
      >>> d = Directory('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
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
        response = requests.get(url, params=params, headers=self.headers).json()

        if response['service_meta']['error_text']:
            raise ValueError(response['service_meta']['error_text'])

        return response

    def search(self, params):
        """Return a list of person objects for the given search params.

        >>> people = d.search({'first_name': 'tobias', 'last_name': 'funke'})
        """
        self._request(ENDPOINTS['SEARCH'], params)
    def detail_search(self, params):
        """Return a detailed list of person objects for the given search params, by performing
        a regular search, and then requesting details for each result.

        >>> people_detailed = d.detail_search({'first_name': 'tobias', 'last_name': 'funke'})
        """

        response = self._request(ENDPOINTS['SEARCH'], params)
        result_data = []
        for person in response['result_data']:
            try:
                detail = self.person(person['person_id'])
                result_data.append(detail)
            except ValueError:
                pass
        response['result_data'] = result_data
        return response;

    def person_details(self, person_id):
        """Return a detailed person object corresponding to the id. ID should be a string.

        >>> instructor = d.person('jhs878sfd03b38b0d463b16320b5e438')
        """
        response = self._request(path.join(ENDPOINTS['DETAILS'], person_id))
        return response['result_data'][0]
