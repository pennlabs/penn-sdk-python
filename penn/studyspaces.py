import requests
import json

from bs4 import BeautifulSoup


BASE_URL = "http://libcal.library.upenn.edu"


class StudySpaces(object):
    def __init__(self):
        pass

    def get_buildings(self):
        """Returns a list of building IDs, building names, and services."""

        soup = BeautifulSoup(requests.get("{}/spaces".format(BASE_URL)).content, "html5lib")
        options = soup.find("select", {"id": "lid"}).find_all("option")
        return [{"id": int(opt["value"]), "name": str(opt.text), "service": "libcal"} for opt in options]

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
        rooms = {}
        for row in resp.json():
            room_id = int(row["resourceId"][4:])
            if room_id not in rooms:
                rooms[room_id] = []
            rooms[room_id].append({
                "start": row["start"],
                "end": row["end"],
                "booked": row["status"] != 0
            })
        return [{"room_id": k, "times": v} for k, v in rooms.items()]
