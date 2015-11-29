from requests import get
import re


class APIError(ValueError):
    pass


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
        """Make a signed request to the API, raise any API errors, and
        returning a tuple of (data, metadata)
        """
        response = get(url, params=params, headers=self.headers, timeout=10)
        if response.status_code != 200:
            raise ValueError('Request to {} returned {}'
                             .format(response.url, response.status_code))

        response = response.json()

        error_text = response['service_meta']['error_text']
        if error_text:
            raise APIError(error_text)

        return response

    def validate(self, validation_dict, params):
        errors = {}
        params_map = validation_dict['acceptable_search_url_parameters_map']
        for param in params:
            if param not in params_map:
                errors[param] = 'This is not a valid parameter'
            else:
                m = re.match(r"Use one of the values from the map (\w+)",
                             params_map[param], flags=re.IGNORECASE)
                if m:
                    map_name = m.group(1)
                    d = validation_dict[map_name]
                    if params[param] not in d and params[param].upper() not in d:
                        errors[param] = 'Invalid value for this parameter'
        return errors
