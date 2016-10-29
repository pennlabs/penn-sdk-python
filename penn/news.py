from .base import WrapperBase


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/"
ENDPOINTS = {
    'SEARCH': BASE_URL + 'news_events_maps'
}


class News(WrapperBase):
    """The client for the News Search API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn import News
      >>> n = News('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """

    def search(self, keyword):
        """Return all news related to the provided query.

        :param keyword:
            The keyword for your news search

        >>> results = n.search('interview')
        """
        params = {
            "source": "news",
            "description": keyword
        }

        data = self._request(ENDPOINTS['SEARCH'], params)
        data['result_data'] = [res for res in data['result_data'] if isinstance(res, dict)]
        return data
