import requests
import datetime
import json
import pytz
import re
import six
import pkg_resources

from bs4 import BeautifulSoup


BASE_URL = "https://libcal.library.upenn.edu"


class StudySpacesV2(object):
    """Used for interacting with the library libcal api.

    Usage::

      >>> from penn import StudySpacesV2
      >>> s = StudySpacesV2('LIBCAL_CLIENT_ID', 'LIBCAL_CLIENT_SECRET')
    """

    def __init__(self, client_id, client_secret):
        self.token = None
        self.expiration = None
        self.client_id = client_id
        self.client_secret = client_secret

    def _obtain_token(self):
        """Obtain an auth token from client id and client secret."""

        # don't renew token if hasn't expired yet
        if self.expiration and self.expiration > datetime.datetime.now():
            return

        resp = requests.post("https://api2.libcal.com/1.1/oauth/token", data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }).json()
        self.expiration = datetime.datetime.now() + datetime.timedelta(seconds=resp["expires_in"])
        self.token = resp["access_token"]

    def _request(self, *args, **kwargs):
        """Make a signed request to the libcal API."""
        if not self.token:
            self._obtain_token()

        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }

        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        resp = requests.request(*args, **kwargs)
        if resp.status_code == 401 and not kwargs.get("no_token"):
            self._obtain_token()
            kwargs["no_token"] = True
            self._request(*args, **kwargs)
        return resp

    def get_buildings(self):
        """Returns a list of location IDs and names."""
        resp = self._request("GET", "https://api2.libcal.com/1.1/space/locations").json()
        return [x for x in resp if x["public"] == 1]

    def get_rooms(self, lid):
        resp = self._request("GET", "https://api2.libcal.com/1.1/space/categories/{}".format(lid))
        categories = resp.json()[0]["categories"]
        id_to_category = {i["cid"]: i["name"] for i in categories}
        categories = ",".join([str(x["cid"]) for x in categories])
        resp = self._request("GET", "https://api2.libcal.com/1.1/space/category/{}".format(categories))
        output = {"id": lid, "categories": []}
        for category in resp.json():
            cat_out = {"cid": category["cid"], "name": id_to_category[category["cid"]], "rooms": []}
            items = category["items"]
            items = ",".join([str(x) for x in items])
            resp = self._request("GET", "https://api2.libcal.com/1.1/space/item/{}?availability".format(items))
            for room in resp.json():
                if "image" in room and room["image"]:
                    room["image"] = "https:" + room["image"]
                if "formid" in room:
                    del room["formid"]
                cat_out["rooms"].append(room)
            output["categories"].append(cat_out)
        return output

    def book_room(self, item, start, end, fname, lname, email, nickname, custom={}, test=False):
        data = {
            "start": start,
            "fname": fname,
            "lname": lname,
            "email": email,
            "nickname": nickname,
            "bookings": [
                {
                    "id": item,
                    "to": end
                }
            ],
            "test": test
        }
        data.update(custom)
        resp = self._request("POST", "https://api2.libcal.com/1.1/space/reserve", json=data)
        return resp.json()


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

        location_path = pkg_resources.resource_filename("penn", "data/locations.json")
        with open(location_path, "r") as locations:
            return json.loads(locations.read())
        # soup = BeautifulSoup(requests.get("{}/spaces".format(BASE_URL)).content, "html5lib")
        # options = soup.find("select", {"id": "lid"}).find_all("option")
        # return [{"id": int(opt["value"]), "name": str(opt.text), "service": "libcal"} for opt in options if int(opt["value"]) > 0]

    def book_room(self, building, room, start, end, firstname, lastname, email, groupname, phone, size, fake=False):
        """Books a room given the required information.

        :param building:
            The ID of the building the room is in.
        :type building: int
        :param room:
            The ID of the room to book.
        :type room: int
        :param start:
            The start time range of when to book the room.
        :type start: datetime
        :param end:
            The end time range of when to book the room.
        :type end: datetime
        :param fake:
            If this is set to true, don't actually book the room. Default is false.
        :type fake: bool
        :returns:
            Boolean indicating whether the booking succeeded or not.
        :raises ValueError:
            If one of the fields is missing or incorrectly formatted, or if the server fails to book the room.
        """

        data = {
            "formData[fname]": firstname,
            "formData[lname]": lastname,
            "formData[email]": email,
            "formData[nick]": groupname,
            "formData[q2533]": phone,
            "formData[q2555]": size,
            "forcedEmail": ""
        }

        try:
            room_obj = self.get_room_id_name_mapping(building)[room]
        except KeyError:
            raise ValueError("No room with id {} found in building with id {}!".format(room, building))

        if room_obj["lid"] != building:
            raise ValueError("Mismatch between building IDs! (expected {}, got {})".format(building, room_obj["lid"]))

        room_data = {
            "id": 1,
            "eid": room,
            "gid": room_obj["gid"],
            "lid": room_obj["lid"],
            "start": start.strftime("%Y-%m-%d %H:%M"),
            "end": end.strftime("%Y-%m-%d %H:%M")
        }

        for key, val in room_data.items():
            data["bookings[0][{}]".format(key)] = val

        if fake:
            return True

        resp = requests.post("{}/ajax/space/book".format(BASE_URL), data)
        resp_data = resp.json()
        if resp_data.get("success"):
            return True
        else:
            if "error" in resp_data:
                raise ValueError(resp_data["error"])
            else:
                raise ValueError(re.sub('<.*?>', '', resp_data.get("msg").strip()).strip())

    @staticmethod
    def parse_date(date):
        """Converts library system dates into timezone aware Python datetime objects.

        :param date:
            A library system date in the format '2018-01-25 12:30:00'.
        :type date: datetime
        :returns:
            A timezone aware python datetime object.
        """

        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return pytz.timezone("US/Eastern").localize(date)

    @staticmethod
    def get_room_id_name_mapping(building):
        """Returns a dictionary mapping id to name, thumbnail, and capacity.

        The dictionary also contains information about the lid and gid, which are used in the booking process.

        :param building:
            The ID of the building to fetch rooms for.
        :type building: int
        :returns:
            A list of rooms, with each item being a dictionary that contains the room id and available times.
        """

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
            room_gid = int(items["gid"])
            room_lid = int(items["lid"])

            out[room_id] = {
                "name": title,
                "gid": room_gid,
                "lid": room_lid,
                "thumbnail": thumbnail or None,
                "capacity": int(items["capacity"])
            }
        return out

    def get_rooms(self, building, start, end):
        """Returns a dictionary matching all rooms given a building id and a date range.

        The resulting dictionary contains both rooms that are available and rooms that already have been booked.

        :param building:
            The ID of the building to fetch rooms for.
        :type building: int
        :param start:
            The start date of the range used to filter available rooms.
        :type start: datetime
        :param end:
            The end date of the range used to filter available rooms.
        :type end: datetime
        """

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
