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
        url = "{}{}".format(BASE_URL, "/reservations/")
        cookies = dict(sessionid=sessionid)

        try:
            resp = requests.get(url, cookies=cookies)
        except resp.exceptions.HTTPError as error:
            raise APIError("Server Error: {}".format(error))

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
        """Deletes a Wharton GSR Booking for a given booking and session id"""
        url = "{}{}{}/".format(BASE_URL, "/delete/", booking_id)
        cookies = dict(sessionid=sessionid)

        try:
            resp = requests.get(url, cookies=cookies, headers={'Referer': '{}{}'.format(BASE_URL, "/reservations/")})
        except resp.exceptions.HTTPError as error:
            raise APIError("Server Error: {}".format(error))

        if resp.status_code == 404:
            raise APIError("Booking could not be found on server.")

        html = resp.content.decode("utf8")
        if "https://weblogin.pennkey.upenn.edu" in html:
            raise APIError("Wharton Auth Failed. Session ID is not valid.")

        resp.raise_for_status()

        soup = BeautifulSoup(html, "html5lib")
        middleware_token = soup.find("input", {'name': "csrfmiddlewaretoken"}).get('value')

        csrftoken = resp.cookies['csrftoken']
        cookies2 = {'sessionid': sessionid, 'csrftoken': csrftoken}
        headers = {'Referer': url}
        payload = {'csrfmiddlewaretoken': middleware_token}

        try:
            resp2 = requests.post(url, cookies=cookies2, data=payload, headers=headers)
        except resp2.exceptions.HTTPError as error:
            raise APIError("Server Error: {}".format(error))

        return "success"

    def get_wharton_gsrs(self, sessionid, date):
        if date:
            date += " 05:00"
        else:
            date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%S")
        resp = requests.get('https://apps.wharton.upenn.edu/gsr/api/app/grid_view/', params={
            'search_time': date
        }, cookies={
            'sessionid': sessionid
        })
        if resp.status_code == 200:
            return resp.json()
        else:
            raise APIError('Remote server returned status code {}.'.format(resp.status_code))

    def switch_format(self, gsr):
        if "error" in gsr:
            return gsr
        rooms = {
            "cid": 1,
            "name": "Huntsman Hall",
            "rooms": []
        }

        for time in gsr["times"]:
            for entry in time:
                entry["name"] = "GSR " + entry["room_number"]
                del entry["room_number"]
                start_time_str = entry["start_time"]
                end_time = datetime.datetime.strptime(start_time_str[:-6], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(minutes=30)
                end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S") + "-05:00"
                time = {
                    "available": not entry["reserved"],
                    "start": entry["start_time"],
                    "end": end_time_str,
                }
                exists = False
                for room in rooms["rooms"]:
                    if room["name"] == entry["name"]:
                        room["times"].append(time)
                        exists = True
                if not exists:
                    del entry["booked_by_user"]
                    del entry["building"]
                    if "reservation_id" in entry:
                        del entry["reservation_id"]
                    entry["lid"] = 1
                    entry["capacity"] = 5
                    entry["room_id"] = entry["id"]
                    del entry["id"]
                    entry["times"] = [time]
                    del entry["reserved"]
                    del entry["end_time"]
                    del entry["start_time"]
                    rooms["rooms"].append(entry)
        return {"categories": [rooms]}

    def get_wharton_gsrs_formatted(self, sessionid):
        gsrs = self.get_wharton_gsrs(sessionid, None)
        return self.switch_format(gsrs)
