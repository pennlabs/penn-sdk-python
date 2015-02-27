from requests import get
import json

class WrapperBase(object):

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
        response = get(url, params=params, headers=self.headers)
        if response.status_code != 200:
            raise ValueError('Request to {} returned {}'.format(response.url, response.status_code))

        response = response.json()

        if response['service_meta']['error_text']:
            raise ValueError(response['service_meta']['error_text'])

        return response
