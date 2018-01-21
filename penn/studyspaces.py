import requests
import json

from bs4 import BeautifulSoup


BASE_URL = "http://libcal.library.upenn.edu"


class StudySpaces(object):
    def __init__(self):
        pass

    def get_buildings(self):
        """Returns a dictionary matching building IDs to their names."""

        soup = BeautifulSoup(requests.get("{}/spaces".format(BASE_URL)).content, "html5lib")
        options = soup.find("select", {"id": "lid"}).find_all("option")
        return {int(option["value"]): str(option.text) for option in options}

    def get_rooms(self, building, start, end):
        """Returns a dictionary matching all rooms given a building id and a date range."""

        room_endpoint = "{}/process_equip_p_availability.php".format(BASE_URL)
        data = {
            "lid": building,
            "gid": 0,
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "bookings": []
        }
        resp = requests.post(room_endpoint, data=json.dumps(data), headers={'Referer': "{}/spaces?lid={}".format(BASE_URL, building)})
        return resp.json()
