"""A module for consuming the Penn Registrar API"""
from os import path
import requests


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/"
ENDPOINTS = {
    'CATALOG': BASE_URL + 'course_info',
    'SEARCH': BASE_URL + 'course_section_search',
    'SEARCH_PARAMS': BASE_URL + 'course_section_search_parameters'
}

class Registrar(object):
    """The client for the Registrar API
       Properties:
          bearer: The user code for the API
          token: The password code for the API
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

    def _iter_response(self, url, params=None):
        """Return an enumerable that iterates through a multi-page API request"""
        if params is None:
            params = {}
        params['page_number'] = 1

        # Last page lists itself as next page
        while True:
            response = self._request(url, params)

            for item in response['result_data']:
                yield item

            # Last page lists itself as next page
            if response['service_meta']['next_page_number'] == params['page_number']:
                break

            params['page_number'] += 1

    def search(self, params):
        """Return an iterable of section objects for the given search params"""
        return self._iter_response(ENDPOINTS['SEARCH'], params)

    def course(self, dept, course_number):
        """Return a course-info object"""
        return self._request(path.join(ENDPOINTS['CATALOG'], dept, course_number))['result_data'][0]

    def department(self, dept):
        """Return an iterable of all course-info objects in a department, in no
        particular order"""
        return self._iter_response(path.join(ENDPOINTS['CATALOG'], dept))

    def section(self, dept, course_number, sect_number):
        """Return a single section object for the given section"""
        section_id = dept + course_number + sect_number
        sections = self.search({'course_id': section_id})
        try:
            return next(sections)
        except StopIteration:
            raise ValueError('Section %s not found' % section_id)

    def search_params(self):
        """Return a map of possible search params to a map from their possible values to
        their descriptions."""
        return self._request(ENDPOINTS['SEARCH_PARAMS'])['result_data'][0]
