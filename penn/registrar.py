from os import path
import requests
from base import WrapperBase


BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/"
ENDPOINTS = {
    'CATALOG': BASE_URL + 'course_info',
    'SEARCH': BASE_URL + 'course_section_search',
    'SEARCH_PARAMS': BASE_URL + 'course_section_search_parameters'
}

class Registrar(WrapperBase):
    """The client for the Registrar. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn.registrar import Registrar
      >>> r = Registrar('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """
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
        """Return a generator of section objects for the given search params.

        >>> cis100s = r.search({'course_id': 'cis', 'course_level_at_or_below': '200'})
        """
        return self._iter_response(ENDPOINTS['SEARCH'], params)

    def course(self, dept, course_number):
        """Return an object of semester-independent course info. All arguments should be strings.

        >>> cis120 = r.course('cis', '120')
        """
        response = self._request(path.join(ENDPOINTS['CATALOG'], dept, course_number))
        return response['result_data'][0]

    def department(self, dept):
        """Return an iterator of all course-info objects in a department, in no particular order.
        """
        return self._iter_response(path.join(ENDPOINTS['CATALOG'], dept))

    def section(self, dept, course_number, sect_number):
        """Return a single section object for the given section. All arguments should be
        strings. Throws a `ValueError` if the section is not found.

        >>> lgst101_bfs = r.course('lgst', '101', '301')
        """
        section_id = dept + course_number + sect_number
        sections = self.search({'course_id': section_id})
        try:
            return next(sections)
        except StopIteration:
            raise ValueError('Section %s not found' % section_id)



    def search_params(self):
        """Return a dictionary of possible search parameters and their  possible values and
        descriptions.
        """
        return self._request(ENDPOINTS['SEARCH_PARAMS'])['result_data'][0]
