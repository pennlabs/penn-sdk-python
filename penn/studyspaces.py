import requests
import datetime
import json
import pytz
import re
import six

from bs4 import BeautifulSoup


BASE_URL = "https://libcal.library.upenn.edu"


class StudySpaces(object):
    """Used for interacting with the UPenn library GSR booking system.

    Usage::

      >>> from penn import StudySpaces
      >>> s = StudySpaces()
    """

    def __init__(self):
        pass

    def get_buildings(self):
        """Returns a list of building IDs, building names, and services."""

        soup = BeautifulSoup(requests.get("{}/spaces".format(BASE_URL)).content, "html5lib")
        options = soup.find("select", {"id": "lid"}).find_all("option")
        return [{"id": int(opt["value"]), "name": str(opt.text), "service": "libcal"} for opt in options]

    @staticmethod
    def parse_date(date):
        """Converts library system dates into timezone aware Python datetime objects."""

        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return pytz.timezone("US/Eastern").localize(date)

    @staticmethod
    def get_room_id_name_mapping(building):
        """ Returns a dictionary mapping id to name, thumbnail, and capacity. """

        data = requests.get("{}/spaces?lid={}".format(BASE_URL, building)).content.decode("utf8")
        # find all of the javascript room definitions
        out = {}
        for item in re.findall(r"resources.push\(((?s).*?)\);", data, re.MULTILINE):
            # parse all of the room attributes
            items = {k: v for k, v in re.findall(r'(\w+?):\s*(.*?),', item)}

            # room name formatting
            title = items["title"][1:-1]
            title = title.encode().decode("unicode_escape" if six.PY3 else "string_escape")
            title = re.sub(r" \(Capacity [0-9]+\)", r"", title)

            # turn thumbnail into proper url
            thumbnail = items["thumbnail"][1:-1]
            if thumbnail:
                thumbnail = "https:" + thumbnail

            room_id = int(items["eid"])
            out[room_id] = {
                "name": title,
                "thumbnail": thumbnail or None,
                "capacity": int(items["capacity"])
            }
        return out

    def get_rooms(self, building, start, end):
        """Returns a dictionary matching all rooms given a building id and a date range."""

        if start.tzinfo is None:
            start = pytz.timezone("US/Eastern").localize(start)
        if end.tzinfo is None:
            end = pytz.timezone("US/Eastern").localize(end)

        mapping = self.get_room_id_name_mapping(building)
        room_endpoint = "{}/process_equip_p_availability.php".format(BASE_URL)
        data = {
            "lid": building,
            "gid": 0,
            "start": start.strftime("%Y-%m-%d"),
            "end": (end + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            "bookings": []
        }
        resp = requests.post(room_endpoint, data=json.dumps(data), headers={'Referer': "{}/spaces?lid={}".format(BASE_URL, building)})
        rooms = {}
        for row in resp.json():
            room_id = int(row["resourceId"][4:])
            if room_id not in rooms:
                rooms[room_id] = []
            room_start = self.parse_date(row["start"])
            room_end = self.parse_date(row["end"])
            if start <= room_start <= end:
                rooms[room_id].append({
                    "start": room_start.isoformat(),
                    "end": room_end.isoformat(),
                    "available": row["status"] == 0
                })
        out = []
        for k, v in rooms.items():
            item = {
                "room_id": k,
                "times": v
            }
            if k in mapping:
                item.update(mapping[k])
            out.append(item)
        return out
