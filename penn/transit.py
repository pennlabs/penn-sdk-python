"""A module for consuming the Penn Transit API"""
from .base import WrapperBase

BASE_URL = "https://esb.isc-seo.upenn.edu/8091/open_data/transit/"
ENDPOINTS = {
    'APC': BASE_URL + 'apc',
    'MDT': BASE_URL + 'mdt',
    'TRANSAPC': BASE_URL + 'transapc',
    'STOPINVENTORY': BASE_URL + 'stopinventory',
    'STOPTIMES': BASE_URL + 'stoptimes',
    'PREDICTION': BASE_URL + '511/Prediction',
    'CONFIGURATION': BASE_URL + '511/Configuration'
}


class Transit(WrapperBase):
    """The client for Transit. Used to make requests to the API.

    :param bearer: The user code for the API
    :param token: The password code for the API

    Usage::

      >>> from penn import Transit
      >>> trans = Transit('MY_USERNAME_TOKEN', 'MY_PASSWORD_TOKEN')
    """

    @staticmethod
    def format_date(date):
        return date.strftime("%m/%d/%Y") + " " + date.strftime("%H:%M:%S")

    def apc(self, start_date, end_date):
        """Return all APC data packets in date range

        :param start_date:
            The starting date for the query.
        :param end_date:
            The end date for the query.
        >>> import datetime
        >>> today = datetime.date.today()
        >>> trans.apc(today - datetime.timedelta(days=1), today))
        """
        params = {
            'start': self.format_date(start_date),
            'end': self.format_date(end_date)
        }
        response = self._request(ENDPOINTS['APC'], params)
        return response

    def mdt(self, start_date, end_date):
        """Return all MDT data packets in date range

        :param start_date:
            The starting date for the query.
        :param end_date:
            The end date for the query.
        >>> import datetime
        >>> today = datetime.date.today()
        >>> trans.mdt(today - datetime.timedelta(days=1), today))
        """

        params = {
            'start': self.format_date(start_date),
            'end': self.format_date(end_date)
        }
        response = self._request(ENDPOINTS['MDT'], params)
        return response

    def transapc(self, start_date, end_date):

        """Return detail of boardings, alightings, by vehicle and stop,
        including the passenger load leaving the stop (this is only for
        vehicles equipped with APC hardware)

        :param start_date:
            The starting date for the query.
        :param end_date:
            The end date for the query.
        >>> import datetime
        >>> today = datetime.date.today()
        >>> trans.transapc(today - datetime.timedelta(days=1), today))

        """
        params = {
            'start': self.format_date(start_date),
            'end': self.format_date(end_date)
        }
        response = self._request(ENDPOINTS['TRANSAPC'], params)
        return response

    def stopinventory(self):
        """Return a list all transit stops.

        >>> stops = trans.stopinventory()
        """
        response = self._request(ENDPOINTS['STOPINVENTORY'])
        return response

    def prediction(self):
        """Return route data and time predictions

        >>> predictions = trans.prediction()
        """
        response = self._request(ENDPOINTS['PREDICTION'])
        return response

    def configuration(self):
        """Return route configuration info

        >>> route_config = trans.configuration()
        """
        response = self._request(ENDPOINTS['CONFIGURATION'])
        return response

    def stoptimes(self, start_date, end_date):
        """Return all stop times in the date range

        :param start_date:
            The starting date for the query.
        :param end_date:
            The end date for the query.
        >>> import datetime
        >>> today = datetime.date.today()
        >>> trans.stoptimes(today - datetime.timedelta(days=1), today)
        """
        params = {
            'start': self.format_date(start_date),
            'end': self.format_date(end_date)
        }
        response = self._request(ENDPOINTS['STOPTIMES'], params)
        return response
