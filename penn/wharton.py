import requests
import datetime

from bs4 import BeautifulSoup
from .base import APIError


BASE_URL = "https://apps.wharton.upenn.edu/gsr"


class Wharton(object):
    """Used for interacting with the Wharton GSR site.

    Usage::

      >>> from penn import Wharton
      >>> s = Wharton()
    """

    def get_reservations(self, sessionid):
        """Returns a list of location IDs and names."""
        url = "{}{}".format(BASE_URL, "/reservations")
        cookies = dict(sessionid=sessionid)
        resp = requests.get(url, cookies=cookies)
        if "error" in resp:
            raise APIError("Server Error: {}, {}".format(resp["error"], resp.get("error_description")))

        html = resp.content.decode("utf8")

        if "https://weblogin.pennkey.upenn.edu" in html:
            raise APIError("Wharton Auth Failed. Session ID is not valid.")

        soup = BeautifulSoup(html, "html5lib")
        reservations = []
        media = soup.find_all("div", {'class': "Media-body"})
        for res in media:
            times = res.find_all("span", {'class': "list-view-item__end-time"})
            reservation = {
                "date": res.find("span", {'class': "list-view-item__start-time u-display-block"}).get_text(),
                "startTime": times[0].get_text(),
                "endTime": times[1].get_text(),
                "location": res.find("span", {'class': "list-view-item-building"}).get_text(),
                "booking_id": int(res.find("a")['href'].split("delete/")[1][:-1])
            }
            reservations.append(reservation)
        return reservations

    def delete_booking(self, sessionid, booking_id):
        """Returns a list of location IDs and names."""
        url = "{}{}{}".format(BASE_URL, "/delete/", booking_id)
        print(url)
        cookies = dict(sessionid=sessionid)
        
        try:
            resp = requests.get(url, cookies=cookies)
        except resp.exceptions.HTTPError as error:
            raise APIError("Server Error: {}".format(error))

        if resp.status_code == 404:
            raise APIError("Booking could not be found on server.")

        html = resp.content.decode("utf8")
        if "https://weblogin.pennkey.upenn.edu" in html:
            raise APIError("Wharton Auth Failed. Session ID is not valid.")

        soup = BeautifulSoup(html, "html5lib")
        print(resp.cookies)
        csrftoken = resp.cookies['csrftoken']
        middleware_token = soup.find("input", {'name': "csrfmiddlewaretoken"}).get('value')
        cookies2 = {'sessionid': sessionid, 'csrftoken': csrftoken}

        try:
            resp2 = requests.post(url, cookies=cookies2, data={'csrfmiddlewaretoken': middleware_token})
        except resp.exceptions.HTTPError as error:
            raise APIError("Server Error: {}".format(error))

        print(resp2.content.decode("utf8"))

        return "success"
