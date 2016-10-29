from .base import WrapperBase

BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/"
ENDPOINTS = {
    'SEARCH': BASE_URL + 'news_events_maps'
}


class Map(WrapperBase):
    """The client for the Map Search API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn import Map
      >>> n = Map('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """

    def search(self, keyword):
        """Return all buildings related to the provided query.

        :param keyword:
            The keyword for your map search

        >>> results = n.search('Harrison')
        """
        params = {
            "source": "map",
            "description": keyword
        }
        data = self._request(ENDPOINTS['SEARCH'], params)
        data['result_data'] = [res for res in data['result_data'] if isinstance(res, dict)]
        return data
