from os import path
from .base import WrapperBase
from nameparser import HumanName


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/"
ENDPOINTS = {
    'SEARCH': BASE_URL + 'directory',
    'DETAILS': BASE_URL + 'directory_person_details',
}


class Directory(WrapperBase):
    """The client for the Directory. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn import Directory
      >>> d = Directory('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """

    def search(self, params, standardize=False):
        """Get a list of person objects for the given search params.

        :param params: Dictionary specifying the query parameters
        :param standardize: Whether to standardize names and other features,
            currently disabled for backwards compatibility.

        >>> people = d.search({'first_name': 'tobias', 'last_name': 'funke'})
        """
        resp = self._request(ENDPOINTS['SEARCH'], params)
        if not standardize:
            return resp
        # Standardization logic
        for res in resp['result_data']:
            name = HumanName(res['list_name'])
            name.capitalize()
            res['list_name'] = str(name)
        return resp

    def detail_search(self, params):
        """Get a detailed list of person objects for the given search params.

        :param params:
            Dictionary specifying the query parameters

        >>> people_detailed = d.detail_search({'first_name': 'tobias', 'last_name': 'funke'})
        """

        response = self._request(ENDPOINTS['SEARCH'], params)
        result_data = []
        for person in response['result_data']:
            try:
                detail = self.person_details(person['person_id'])
            except ValueError:
                pass
            else:
                result_data.append(detail)

        response['result_data'] = result_data
        return response

    def person_details(self, person_id):
        """Get a detailed person object

        :param person_id:
            String corresponding to the person's id.

        >>> instructor = d.person('jhs878sfd03b38b0d463b16320b5e438')
        """
        return self._request(path.join(ENDPOINTS['DETAILS'], person_id))
