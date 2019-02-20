import requests
import datetime

from bs4 import BeautifulSoup
from .base import APIError


BASE_URL = "https://libcal.library.upenn.edu"
API_URL = "https://api2.libcal.com"

LOCATION_BLACKLIST = set([3620, 2636, 2611, 3217, 2637, 2634])
ROOM_BLACKLIST = set([7176, 16970, 16998, 17625])


class StudySpaces(object):
    """Used for interacting with the library libcal api.

    Usage::

      >>> from penn import StudySpaces
      >>> s = StudySpaces('LIBCAL_CLIENT_ID', 'LIBCAL_CLIENT_SECRET')
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

        resp = requests.post("{}/1.1/oauth/token".format(API_URL), data={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }).json()

        if "error" in resp:
            raise APIError("LibCal Auth Failed: {}, {}".format(resp["error"], resp.get("error_description")))

        self.expiration = datetime.datetime.now() + datetime.timedelta(seconds=resp["expires_in"])
        self.token = resp["access_token"]

    def _request(self, *args, **kwargs):
        """Make a signed request to the libcal API."""
        if not self.token:
            self._obtain_token()

        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }

        # add authorization headers
        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        # add api site to url
        args = list(args)
        if not args[1].startswith("http"):
            args[1] = "{}{}".format(API_URL, args[1])

        has_no_token = kwargs.get("no_token")
        if has_no_token:
            del kwargs["no_token"]
        resp = requests.request(*args, **kwargs)
        if resp.status_code == 401 and not has_no_token:
            self._obtain_token()
            kwargs["no_token"] = True
            self._request(*args, **kwargs)
        return resp

    def get_buildings(self):
        """Returns a list of location IDs and names."""
        resp = self._request("GET", "/1.1/space/locations").json()
        out = []
        for x in resp:
            if x["lid"] in LOCATION_BLACKLIST:
                continue
            if x["public"] == 1:
                del x["public"]
                x["service"] = "libcal"
                out.append(x)
        return out

    def get_rooms(self, lid, start=None, end=None):
        """Returns a list of rooms and their availabilities, grouped by category.

        :param lid: The ID of the location to retrieve rooms for.
        :type lid: int
        :param start: The start range for the availabilities to retrieve, in YYYY-MM-DD format.
        :type start: str
        :param end: The end range for the availabilities to retrieve, in YYYY-MM-DD format.
        :type end: str
        """
        range_str = "availability"
        if start:
            start_datetime = datetime.datetime.combine(datetime.datetime.strptime(start, "%Y-%m-%d").date(), datetime.datetime.min.time())
            range_str += "=" + start
            if end and not start == end:
                range_str += "," + end
        else:
            start_datetime = None

        resp = self._request("GET", "/1.1/space/categories/{}".format(lid)).json()
        if "error" in resp:
            raise APIError(resp["error"])
        output = {"id": lid, "categories": []}

        # if there aren't any rooms associated with this location, return
        if len(resp) < 1:
            return output

        if "error" in resp[0]:
            raise APIError(resp[0]["error"])

        if "categories" not in resp[0]:
            return output

        categories = resp[0]["categories"]
        id_to_category = {i["cid"]: i["name"] for i in categories}
        categories = ",".join([str(x["cid"]) for x in categories])
        resp = self._request("GET", "/1.1/space/category/{}".format(categories))
        for category in resp.json():
            cat_out = {"cid": category["cid"], "name": id_to_category[category["cid"]], "rooms": []}

            # ignore equipment categories
            if cat_out["name"].endswith("Equipment"):
                continue

            items = category["items"]
            items = ",".join([str(x) for x in items])
            resp = self._request("GET", "/1.1/space/item/{}?{}".format(items, range_str))
            for room in resp.json():
                if room["id"] in ROOM_BLACKLIST:
                    continue
                # prepend protocol to urls
                if "image" in room and room["image"]:
                    if not room["image"].startswith("http"):
                        room["image"] = "https:" + room["image"]
                # convert html descriptions to text
                if "description" in room:
                    description = room["description"].replace(u'\xa0', u' ')
                    room["description"] = BeautifulSoup(description, "html.parser").text.strip()
                # remove extra fields
                if "formid" in room:
                    del room["formid"]
                # enforce date filter
                # API returns dates outside of the range, fix this manually
                if start_datetime:
                    out_times = []
                    for time in room["availability"]:
                        parsed_start = datetime.datetime.strptime(time["from"][:-6], "%Y-%m-%dT%H:%M:%S")
                        if parsed_start >= start_datetime:
                            out_times.append(time)
                    room["availability"] = out_times
                cat_out["rooms"].append(room)
            if cat_out["rooms"]:
                output["categories"].append(cat_out)
        return output

    def book_room(self, item, start, end, fname, lname, email, nickname, custom={}, test=False):
        """Books a room given the required information.

        :param item:
            The ID of the room to book.
        :type item: int
        :param start:
            The start time range of when to book the room, in the format returned by the LibCal API.
        :type start: str
        :param end:
            The end time range of when to book the room, in the format returned by the LibCal API.
        :type end: str
        :param fname:
            The first name of the user booking the room.
        :type fname: str
        :param lname:
            The last name of the user booking the room.
        :type lname: str
        :param email:
            The email of the user booking the room.
        :type email: str
        :param nickname:
            The name of the reservation.
        :type nickname: str
        :param custom:
            Any other custom fields required to book the room.
        :type custom: dict
        :param test:
            If this is set to true, don't actually book the room. Default is false.
        :type test: bool
        :returns:
            Dictionary containing a success and error field.
        """
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
        resp = self._request("POST", "/1.1/space/reserve", json=data)
        out = resp.json()
        if "errors" in out and "error" not in out:
            errors = out["errors"]
            if isinstance(errors, list):
                errors = " ".join(errors)
            out["error"] = BeautifulSoup(errors.replace("\n", " "), "html.parser").text.strip()
            del out["errors"]
        if "results" not in out:
            if "error" not in out:
                out["error"] = None
                out["results"] = True
            else:
                out["results"] = False
        return out

    def cancel_room(self, booking_id):
        """Cancel a room given a booking id.

        :param booking_id: A booking id or a list of booking ids (separated by commas) to cancel.
        :type booking_id: str
        """
        resp = self._request("POST", "/1.1/space/cancel/{}".format(booking_id))
        return resp.json()

    def get_reservations(self, email):
        """Gets reservations for a given email.

        :param email: the email of the user who's reservations are to be fetched
        :type email: str
        """
        
        try:
            resp = self._request("GET", "/1.1/space/bookings?email={}".format(email))
        except resp.exceptions.HTTPError as error:
            raise APIError("Server Error: {}".format(error))
        return resp.json()

    def get_room_info(self, room_ids):
        """Gets room information for a given list of ids.

        :param room_ids: a room id or a list of room ids (comma separated).
        :type room_ids: string
        """
        
        try:
            resp = self._request("GET", "/1.1/space/item/{}".format(room_ids))
            rooms = resp.json()
            for room in rooms:
                if not room["image"].startswith("http"):
                    room["image"] = "https:" + room["image"]

                if "description" in room:
                    description = room["description"].replace(u'\xa0', u' ')
                    room["description"] = BeautifulSoup(description, "html.parser").text.strip()
        except resp.exceptions.HTTPError as error:
            raise APIError("Server Error: {}".format(error))
        return rooms
