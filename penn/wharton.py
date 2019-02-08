import requests
import datetime

from bs4 import BeautifulSoup
from .base import APIError
from flask import jsonify, request


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

    def get_wharton_gsrs(self, sessionid):
        time = request.args.get('date')
        if time:
            time += " 05:00"
        else:
            time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%S")
        resp = requests.get('https://apps.wharton.upenn.edu/gsr/api/app/grid_view/', params={
            'search_time': time
        }, cookies={
            'sessionid': sessionid
        })
        if resp.status_code == 200:
            return resp.json()
        else:
            return {'error': 'Remote server returned status code {}.'.format(resp.status_code)}

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
                time = {
                    "available": entry["reserved"],
                    "end": entry["end_time"],
                    "start": entry["start_time"]
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
                    # entry["gid"] = null
                    # entry["thumbnail"] = null;
                    # entry["description"] = null
                    entry["room_id"] = entry["id"]
                    del entry["id"]
                    entry["times"] = [time]
                    del entry["reserved"]
                    del entry["end_time"]
                    del entry["start_time"]
                    rooms["rooms"].append(entry)
        return {"categories": [rooms]}

    def get_wharton_gsrs_formatted(self, sessionid):
        gsrs = self.get_wharton_gsrs(sessionid)
        return self.switch_format(gsrs)
